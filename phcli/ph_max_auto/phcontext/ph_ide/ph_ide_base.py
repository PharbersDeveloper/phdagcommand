import os
import sys
import ast
import subprocess
import boto3
import json
import time
import uuid
import base64
from enum import Enum

from phcli.ph_errs.ph_err import *
from phcli.ph_max_auto import define_value as dv
from phcli import define_value as phcli_dv
from phcli.ph_max_auto.ph_config.phconfig.phconfig import PhYAMLConfig
from phcli.ph_max_auto.ph_preset_jobs.preset_job_factory import preset_factory
from phcli.ph_aws.ph_sts import PhSts
from phcli.ph_logs.ph_logs import phs3logger, LOG_DEBUG_LEVEL
from phcli.ph_tools.snowflakeId.snowflake import IdWorker


class PhCompleteStrategy(Enum):
    S2C = 'special to common'
    C2S = 'common to special'
    KEEP = 'keep still'


class PhIDEBase(object):
    job_prefix = "/phjobs/"
    combine_prefix = "/phcombines/"
    dag_prefix = "/phdags/"
    upload_prefix = "/upload/"

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.__dict__.update(self.get_absolute_path())
        self.logger.debug('maxauto PhIDEBase init')
        self.logger.debug(self.__dict__)

    def get_workspace_dir(self):
        return os.getenv(dv.ENV_WORKSPACE_KEY, dv.ENV_WORKSPACE_DEFAULT)

    def get_current_project_dir(self):
        return os.getenv(dv.ENV_CUR_PROJ_KEY, dv.ENV_CUR_PROJ_DEFAULT)

    def get_absolute_path(self):
        if 'name' not in self.__dict__ and 'job_full_name' in self.__dict__:
            self.name = self.job_full_name

        project_path = self.get_workspace_dir() + '/' + self.get_current_project_dir()
        job_path = project_path + self.job_prefix + (self.group + '/' if 'group' in self.__dict__.keys() else '') + self.name
        combine_path = project_path + self.combine_prefix + self.name + '/'
        dag_path = project_path + self.dag_prefix + self.name + '/'
        upload_path = project_path + self.upload_prefix + self.name + '/'

        return {
            'project_path': project_path,
            'job_path': job_path,
            'combine_path': combine_path,
            'dag_path': dag_path,
            'upload_path': upload_path,
        }

    def check_path(self, path):
        suffixs = ['', '.ipynb']
        for suffix in suffixs:
            tmp_path = path + suffix
            if os.path.exists(tmp_path):
                override = input('Job "' + tmp_path + '" already existed???want to override???(Y/*)')
                if override.upper() == 'Y':
                    subprocess.call(["rm", "-rf", tmp_path])
                else:
                    self.logger.error('Termination Create')
                    sys.exit()

    def table_driver_runtime_inst(self, runtime):
        from ..ph_runtime.ph_rt_python3 import PhRTPython3
        from ..ph_runtime.ph_rt_r import PhRTR
        table = {
            "python3": PhRTPython3,
            "r": PhRTR,
        }
        return table[runtime]

    def create(self, **kwargs):
        """
        ?????????????????????
        """
        self.logger.debug('maxauto ????????? create ??????')
        self.logger.debug(self.__dict__)

        runtime_inst = self.table_driver_runtime_inst(self.runtime)
        runtime_inst(**self.__dict__).create()

    def choice_complete_strategy(self, special_path, common_path):
        special_last_modify_time = os.path.getmtime(special_path) if os.path.exists(special_path) else 0
        common_last_modify_time = os.path.getmtime(common_path) if os.path.exists(common_path) else 0

        if special_last_modify_time > common_last_modify_time:
            return PhCompleteStrategy.S2C
        elif special_last_modify_time < common_last_modify_time:
            return PhCompleteStrategy.C2S
        else:
            return PhCompleteStrategy.KEEP

    def complete(self, **kwargs):
        """
        ?????????????????????
        """
        self.logger.debug('maxauto ????????? complete ??????')
        self.logger.debug(self.__dict__)

    def run(self, **kwargs):
        """
        ?????????????????????
        """
        self.logger.debug('maxauto ????????? run ??????')
        self.logger.debug(self.__dict__)

        config = PhYAMLConfig(self.job_path)
        config.load_yaml()

        if config.spec.containers.repository == "local":
            timeout = float(config.spec.containers.timeout) * 60
            entry_runtime = config.spec.containers.runtime
            entry_runtime = self.table_driver_runtime_inst(self.runtime)().table_driver_runtime_binary(entry_runtime)
            entry_point = config.spec.containers.code
            entry_point = self.job_path + '/' + entry_point

            cb = [entry_runtime, entry_point]
            for arg in config.spec.containers.args:
                cb.append("--" + arg.key)
                cb.append(str(arg.value))
            for output in config.spec.containers.outputs:
                cb.append("--" + output.key)
                cb.append(str(output.value))
            prc = subprocess.run(cb, timeout=timeout, stderr=subprocess.PIPE)
            if prc.returncode != 0:
                raise Exception(prc.stderr.decode('utf-8'))
            return
        else:
            raise exception_function_not_implement

    def combine(self, **kwargs):
        """
        ?????????????????????
        """
        self.logger.debug('maxauto ????????? combine ??????')
        self.logger.debug(self.__dict__)

        self.check_path(self.combine_path)
        subprocess.call(["mkdir", "-p", self.combine_path])

        def extract_jobs(jobs_str):
            jobs_lst = [job.strip() for job in jobs_str.split(',')]
            jobs = '\n    '.join(['- name: ' + job for job in jobs_lst])
            linkage = ' >> '.join(jobs_lst)
            linkage = '"' + linkage + '"'
            return jobs, linkage

        jobs_str, linkage_str = extract_jobs(self.jobs)
        f_lines = self.phs3.open_object_by_lines(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_PHDAG_FILE)
        with open(self.combine_path + "/phdag.yaml", "w") as file:
            for line in f_lines:
                line = line.replace("$name", self.name) \
                            .replace("$dag_owner", self.owner) \
                            .replace("$dag_tag", self.tag) \
                            .replace("$dag_timeout", self.timeout) \
                            .replace("$linkage", linkage_str) \
                            .replace("$jobs", jobs_str)
                file.write(line + "\n")

    def get_dag_py_file_name(self, key):
        return "ph_dag_" + key + ".py"

    def dag(self, **kwargs):
        """
        ?????????DAG??????
        """
        self.logger.debug('maxauto ????????? dag ??????')
        self.logger.debug(self.__dict__)

        self.check_path(self.dag_path)
        subprocess.call(["mkdir", "-p", self.dag_path])

        config = PhYAMLConfig(self.combine_path, "/phdag.yaml")
        config.load_yaml()

        def get_jobs_conf(config):
            def get_job_conf(name):
                job_full_path = self.project_path + self.job_prefix + name.replace('.', '/')
                if name.startswith('preset.'):
                    job_name = name.lstrip('preset.')
                    ipt_module = __import__('phcli.ph_max_auto.ph_preset_jobs.%s' % (job_name.lower()))
                    ipt_module = getattr(ipt_module, 'ph_max_auto')
                    ipt_module = getattr(ipt_module, 'ph_preset_jobs')
                    ipt_module = getattr(ipt_module, job_name)
                    phconf_buf = getattr(ipt_module, 'phconf_buf')

                    config = PhYAMLConfig()
                    config.load_yaml(phconf_buf(self))
                    return {
                        'name': config.metadata.name,
                        'ide': 'preset',
                        'runtime': config.spec.containers.runtime,
                        'command': config.spec.containers.command,
                        'timeout': config.spec.containers.timeout,
                    }
                elif os.path.isdir(job_full_path):
                    config = PhYAMLConfig(job_full_path)
                    config.load_yaml()
                    return {
                        'name': config.metadata.name,
                        'ide': 'c9',
                        'runtime': config.spec.containers.runtime,
                        'command': config.spec.containers.command,
                        'timeout': config.spec.containers.timeout,
                    }
                else:
                    raise Exception("{} job not found".format(name))

            result = {}
            for job in config.spec.jobs:
                result[job.name] = get_job_conf(job.name)
            return result

        def copy_jobs(jobs_conf):
            ide_dag_copy_job_func_table = {
                'c9': self.ide_table['c9'](**self.__dict__).dag_copy_job,
                'preset': preset_factory,
            }

            # ????????? copy ????????? preset ??? job
            for name, job_info in jobs_conf.items():
                if job_info['ide'] != 'preset':
                    func = ide_dag_copy_job_func_table[job_info['ide']]
                    func(job_name=name, **job_info)

            # ????????? copy ?????? preset ??? job
            for name, job_info in jobs_conf.items():
                if job_info['ide'] == 'preset':
                    func = ide_dag_copy_job_func_table[job_info['ide']]
                    func(self, job_name=name, **job_info)

        def write_dag_pyfile(jobs_conf):
            timeout = config.spec.dag_timeout if config.spec.dag_timeout else sum([float(job['timeout']) for _, job in jobs_conf.items()])
            w = open(self.dag_path + self.get_dag_py_file_name(config.spec.dag_id), "a")
            f_lines = self.phs3.open_object_by_lines(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_PHGRAPHTEMP_FILE)
            for line in f_lines:
                line = line + "\n"
                w.write(
                    line.replace("$alfred_dag_owner", str(config.spec.owner)) \
                        .replace("$alfred_email_on_failure", str(config.spec.email_on_failure)) \
                        .replace("$alfred_email_on_retry", str(config.spec.email_on_retry)) \
                        .replace("$alfred_email", str(config.spec.email)) \
                        .replace("$alfred_retries", str(config.spec.retries)) \
                        .replace("$alfred_retry_delay", str(config.spec.retry_delay)) \
                        .replace("$alfred_dag_id", str(config.spec.dag_id)) \
                        .replace("$alfred_dag_tags", str(','.join(['"'+tag+'"' for tag in config.spec.dag_tag.split(',')]))) \
                        .replace("$alfred_schedule_interval", str(config.spec.schedule_interval)) \
                        .replace("$alfred_description", str(config.spec.description)) \
                        .replace("$alfred_dag_timeout", str(timeout)) \
                        .replace("$alfred_start_date", str(config.spec.start_date))
                )

            jf = self.phs3.open_object_by_lines(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_PHDAGJOB_FILE)
            for jt in config.spec.jobs:
                job_name = jt.name.replace('.', '_')

                for line in jf:
                    line = line + "\n"
                    w.write(
                        line.replace("$alfred_jobs_dir", str(self.name)) \
                            .replace("$alfred_name", str(job_name))
                    )

            for linkage in config.spec.linkage:
                w.write(linkage.replace('.', '_'))
                w.write("\n")

            w.close()

        jobs_conf = get_jobs_conf(config)
        copy_jobs(jobs_conf)
        write_dag_pyfile(jobs_conf)

    def publish(self, **kwargs):
        """
        ?????????????????????
        """
        self.logger.debug('maxauto ????????? publish ??????')
        self.logger.debug(self.__dict__)

        def create_dag_args_step(dag_name, job_full_name, current_random):
            dag_args_step = self.phs3.open_object(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_SFN_DAG_ARGS_STEP_FILE)
            # ???????????????json??????????????????
            json_args = json.dumps(dag_args_step)
            # ????????????
            args_step = json_args.replace("$dag_name", dag_name) \
                .replace("$job_full_name", job_full_name + "_" + current_random)\
                .replace("$no_random_job_full_name", job_full_name)
            # ?????????????????????
            dict_dag_args = eval(json.loads(args_step))
            return dict_dag_args

        def create_args_step(job_full_name, current_random):
            # ???s3?????? lmd_step ?????????
            dag_args_step = self.phs3.open_object(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_SFN_LMD_STEP_FILE)
            # ???????????????json??????????????????
            json_args = json.dumps(dag_args_step)
            # ????????????
            args_step = json_args.replace("$job_full_name", job_full_name + "_" + current_random)
            # ?????????????????????
            dict_args = eval(json.loads(args_step))
            return dict_args

        def create_run_id_step(job_full_names, current_randoms):
            definition_tmp = {
                "StartAt": "",
                "States": {}
            }
            definition_tmp['StartAt'] = "create_run_id"
            first_job_full_name = job_full_names[0]
            first_current_random = current_randoms[0]
            # ???s3?????? lmd_step ?????????
            dag_args_step = self.phs3.open_object(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_SFN_RUN_ID_STEP_FILE)
            # ???????????????json??????????????????
            json_args = json.dumps(dag_args_step)
            # ????????????
            if first_job_full_name.startswith('['):
                if len(first_job_full_name) > 60:
                    first_job_full_name = first_job_full_name[:39]
                args_step = json_args.replace("$first_job_full_name", first_job_full_name + "_" + first_current_random)
            else:
                args_step = json_args.replace("$first_job_full_name", "dag_args_" + first_job_full_name + "_" + first_current_random)
            # ?????????????????????
            definition_tmp_states = eval(json.loads(args_step))
            definition_tmp['States'] = definition_tmp_states
            return definition_tmp

        def create_parallel_step(job_full_name, whole_flows):
            # ??????????????????Parallel??????
            parallel_branches = []
            # ?????????????????????
            parallel_task_list = job_full_name.strip(' []').replace(' ', '').split(',')
            for parallel_task in parallel_task_list:
                for parallel_flow in whole_flows:
                    if parallel_flow.startswith(parallel_task):
                        parallel_task = parallel_flow
                # ??????parallel_task??????randoms
                randoms = []
                flows = []
                # ????????? parallel_task ??? >> ??????
                for parallel_job_name in parallel_task.split('>>'):
                    flows.append(parallel_job_name.strip(" "))
                    snowflake_id = IdWorker(1, 2, 0)
                    randoms.append(str(snowflake_id.get_id()))
                parallel_step = create_step(self.name, flows, randoms, whole_flows)
                parallel_branches.append(parallel_step)
            return parallel_branches

        def create_step(dag_name, job_full_names, randoms, whole_flows):

            definition = {
                        "StartAt": "",
                        "States": {}
                    }

            definition['StartAt'] = "dag_args_" + job_full_names[0] + "_" +randoms[0]
            # ???????????? job_full_name
            for current_index in range(len(job_full_names)):
                # ???????????? job_full_name
                job_full_name = job_full_names[current_index]
                # ????????????job_full_name ??????????????????
                current_random = randoms[current_index]

                # ??????step???args?????? ?????????job???????????????step
                if not job_full_name.startswith('['):
                    # ????????????dag_args???step
                    dict_dag_args = create_dag_args_step(dag_name, job_full_name, current_random)
                    # ??????????????????step?????????definition
                    definition['States'].update(dict_dag_args)
                    dict_args = create_args_step(job_full_name, current_random)
                    definition['States'].update(dict_args)

                # ??????step????????? ??????step?????????
                dag_step = self.phs3.open_object(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_SFN_STEP_FILE)
                json_step = json.dumps(dag_step)
                # ???????????????step??????????????????????????????End
                # ????????????job_full_name???list?????????????????????
                if current_index == len(job_full_names) - 1:
                    # ??????????????????'[' ???????????????????????????????????????
                    if job_full_name.startswith('['):
                        dag_step = self.phs3.open_object(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_SFN_PARALLEL_STEP_FILE)
                        # ??????????????? $next_job_full_name ????????? "$next_job_full_name"
                        dag_step = json.loads(dag_step.replace("$next_job_full_name", "\"$next_job_full_name\""))
                        # ??????parallel??????
                        parallel_branches = create_parallel_step(job_full_name, whole_flows)
                        dag_step['$job_full_name']['Branches'] = parallel_branches
                        json_step = json.dumps(dag_step)
                        if len(job_full_name) > 60:
                            job_full_name = job_full_name[:39]
                        dag_step = json_step.replace("$dag_name", dag_name)\
                            .replace("\"$next_job_full_name\"", "true")\
                            .replace("$next_type", "End")\
                            .replace("$job_full_name", job_full_name + "_" + current_random)
                    else:
                        dag_step = json_step.replace("$dag_name", dag_name)\
                            .replace("$next_job_full_name", "True")\
                            .replace("$next_type", "End")\
                            .replace("$job_full_name", job_full_name + "_" + current_random)

                else:
                    # ???????????? ??????list????????????job_full_name
                    next_index = current_index + 1
                    next_job_full_name = job_full_names[next_index]
                    next_random = randoms[next_index]
                    if job_full_name.startswith('['):
                        dag_step = self.phs3.open_object(dv.TEMPLATE_BUCKET,
                                                         dv.CLI_VERSION + dv.TEMPLATE_SFN_PARALLEL_STEP_FILE)
                        dag_step = json.loads(dag_step.replace("$next_job_full_name", "\"$next_job_full_name\""))
                        parallel_branches = create_parallel_step(job_full_name, whole_flows)
                        dag_step['$job_full_name']['Branches'] = parallel_branches
                        json_step = json.dumps(dag_step)
                        if len(job_full_name) > 60:
                            job_full_name = job_full_name[:39]
                        dag_step = json_step.replace("$dag_name", dag_name) \
                            .replace("$next_job_full_name", "dag_args_" + next_job_full_name + "_" + next_random) \
                            .replace("$next_type", "Next") \
                            .replace("$job_full_name", job_full_name + "_" + current_random)
                        # ???????????????parallel ???????????? parallel dag_step
                    else:
                        if next_job_full_name.startswith('['):
                            if len(next_job_full_name) > 60:
                                next_job_full_name = next_job_full_name[:39]
                            dag_step = json_step.replace("$dag_name", dag_name) \
                                .replace("$next_job_full_name", "\\\"" + next_job_full_name + "_" + next_random + "\\\"" ) \
                                .replace("$next_type", "Next")\
                                .replace("$job_full_name", job_full_name + "_" + current_random)
                        else:
                            dag_step = json_step.replace("$dag_name", dag_name) \
                                .replace("$next_job_full_name", "\\\"dag_args_" + next_job_full_name + "_" + next_random + "\\\"" ) \
                                .replace("$next_type", "Next")\
                                .replace("$job_full_name", job_full_name + "_" + current_random)

                if type(json.loads(dag_step)) == str:
                    dict_dag_step = eval(json.loads(dag_step))
                else:
                    dict_dag_step = json.loads(dag_step)

                definition['States'].update(dict_dag_step)
            return definition


        for key in os.listdir(self.dag_path):
            if os.path.isfile(self.dag_path + key):
                pass
                self.phs3.upload(
                    file=self.dag_path+key,
                    bucket_name=dv.DAGS_S3_BUCKET,
                    object_name=dv.DAGS_S3_PREV_PATH + key
                )
            else:
                # ??????dag
                self.phs3.upload_dir(
                    dir=self.dag_path+key,
                    bucket_name=dv.TEMPLATE_BUCKET,
                    s3_dir=dv.CLI_VERSION + dv.DAGS_S3_PHJOBS_PATH + self.name + "/" + key
                )

            if os.path.isfile(self.dag_path + key):
                # ????????? file ?????? dag ????????? py????????? ??????????????????????????????????????? ??????step????????????
                # ?????????????????????????????????????????????
                whole_flows = []
                # ?????????????????????job?????????
                first_flow = []
                cp_first_flow = []
                # ??????job?????????????????????
                randoms = []

                # ???dag???????????????dag?????????
                with open(self.dag_path + key, "r") as dag_file:
                    line = dag_file.readline()
                    while line:
                        while ">>" in line:
                            whole_flows.append(line.rstrip('\n'))
                            break
                        line = dag_file.readline()

                # ???????????????job?????? ?????????>>
                if not whole_flows:
                    with open(self.dag_path + key, "r") as dag_file:
                        lines = dag_file.readlines()
                        last_line = lines[-1]
                        whole_flows.append(last_line.rstrip('\n'))

                # ???????????????random
                for job_name in whole_flows[0].replace(" ", "").split('>>'):
                    first_flow.append(job_name)
                    cp_first_flow.append(job_name)
                    snowflake_id = IdWorker(1, 2, 0)
                    randoms.append(str(snowflake_id.get_id()))
                # ??????step_function???definition
                definition_states = create_step(self.name, cp_first_flow, randoms, whole_flows)
                # ??????dag????????????step?????????run_id
                definition_tmp = create_run_id_step(cp_first_flow, randoms)
                # ???dag???definition???States?????????run_id???States
                definition_tmp['States'].update(definition_states['States'])
                create_definition = json.dumps(definition_tmp)

                step_client = boto3.client('stepfunctions')
                state_machine_names=[]
                rs = step_client.list_state_machines()
                for stateMachine in rs['stateMachines']:
                    name = stateMachine['name']
                    state_machine_names.append(name)

                if self.name not in state_machine_names:
                    response = step_client.create_state_machine(
                        name=self.name,
                        definition=create_definition,
                        roleArn=dv.DEFAULT_ROLE_ARN,
                        type=dv.DEFAULT_MACHINE_TYPE,
                    )

    def recall(self, **kwargs):
        """
        ?????????????????????
        """
        self.logger.debug('maxauto ????????? recall ??????')
        self.logger.debug(self.__dict__)

        self.phs3.delete_dir(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.DAGS_S3_PHJOBS_PATH + self.name)
        self.phs3.delete_dir(dv.DAGS_S3_BUCKET, dv.DAGS_S3_PREV_PATH + self.get_dag_py_file_name(self.name))

    def online_run(self, **kwargs):
        """
        ????????? online_run ??????
        """
        self.logger.debug('maxauto ????????? online_run ??????')
        self.logger.debug(self.__dict__)
        def write_data(definition, s3_dag_path, job_name, excution_name, job_args_name_list):
            Resource = "arn:aws-cn:states:::elasticmapreduce:addStep.sync"
            Parameters = {
                "ClusterId.$": "$.clusterId",
                "Step": {
                    "Name": "My EMR step",
                    "ActionOnFailure": "CONTINUE",
                    "HadoopJarStep": {
                        "Jar": "command-runner.jar",
                        "Args": ["spark-submit",
                                 "--deploy-mode", "cluster",
                                 "--conf", "spark.driver.cores=1",
                                 "--conf", "spark.driver.memory=1g",
                                 "--conf", "spark.executor.cores=1",
                                 "--conf", "spark.executor.memory=4g",
                                 "--conf", "spark.executor.instances=1",
                                 "--conf", "spark.sql.autoBroadcastJoinThreshold=-1",
                                 "--py-files",
                                 "s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-" + phcli_dv.CLI_CLIENT_VERSION + "-py3.8.egg," + s3_dag_path + "phjob.py",
                                 s3_dag_path + "phmain.py",
                                 "--owner", "default_owner",
                                 "--dag_name", s3_dag_path.split('/')[-3],
                                 "--run_id", s3_dag_path.split('/')[-3] + "_" + excution_name,
                                 "--job_full_name", job_name,
                                 "--job_id", "not_implementation"
                                 ]
                    }
                }
            }
            definition['States'][job_name]['End'] = True
            definition['States'][job_name]['Type'] = "Task"
            definition['States'][job_name]['Resource'] = Resource
            Parameters['Step']['HadoopJarStep']['Args'][len(Parameters['Step']['HadoopJarStep']['Args'])
                                                        :len(
                Parameters['Step']['HadoopJarStep']['Args'])] = job_args_name_list
            definition['States'][job_name]['Parameters'] = Parameters
            definition['States'][job_name]['ResultPath'] = "$.firstStep"
            definition['States'][job_name]['Retry'] = [
                {
                    "ErrorEquals": ["States.ALL"],
                    "IntervalSeconds": 1,
                    "MaxAttempts": 1,
                    "BackoffRate": 1.0
                }
            ]
            definition['States'][job_name] = definition['States'].pop(job_name)

        def write_args(args_list, job_args):
            keys = []
            values = []
            # ??????list??????????????? ????????????dict
            for arg in args_list:
                if args_list.index(arg) % 2 == 0:
                    keys.append(arg)
                elif args_list.index(arg) % 2 == 1:
                    values.append(arg)
            args = zip(keys, values)

            args_dict = dict(args)
            # ????????????dict????????????, ???????????????dict????????????
            for key in args_dict.keys():
                if key.lstrip('--') in job_args.keys():
                    args_dict[key] = job_args[key.lstrip('--')]

            new_key = []
            for args_key in args_dict.keys():
                new_key.append(args_key.lstrip('--'))
            new_args = dict(zip(new_key, args_dict.values()))
            return new_args

        def ast_parse(string):
            """
            ??????json
            :param string: json ?????????
            :return: dict
            """
            ast_dict = {}
            if string != "":
                ast_dict = ast.literal_eval(string.replace(" ", ""))
                for k, v in ast_dict.items():
                    if isinstance(v, str) and v.startswith('{') and v.endswith('}'):
                        ast_dict[k] = ast.literal_eval(v)
            return ast_dict

        # airflow ??????
        self.context = ast_parse(self.context)
        self.args = ast_parse(self.args)

        self.s3_job_path = dv.DAGS_S3_PHJOBS_PATH + self.dag_name + "/" + self.job_full_name
        self.submit_prefix = "s3a://" + dv.TEMPLATE_BUCKET + "/" + dv.CLI_VERSION + self.s3_job_path + "/"

        # stream = self.phs3.open_object(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + self.s3_job_path + "/phconf.yaml")
        # config = PhYAMLConfig()
        # config.load_yaml(stream)
        # self.runtime = config.spec.containers.runtime
        # self.command = config.spec.containers.command
        # self.timeout = config.spec.containers.timeout
        #
        # runtime_inst = self.table_driver_runtime_inst(self.runtime)
        # runtime_inst(**self.__dict__).online_run()


        # step functions ??????
        s3_dag_path = "s3://" + dv.TEMPLATE_BUCKET + "/" + dv.CLI_VERSION + self.s3_job_path + "/"
        job_name = self.name
        definition = {
            "StartAt": "",
            "States": {}
        }
        states = {}
        states[job_name] = {}
        definition['StartAt'] = job_name
        definition['States'] = states
        random_num = "_" + str(uuid.uuid4())
        job_args_name = 'args' + random_num
        # ??? job_args_name ??????list
        job_args_name_list = ['--job_args_name',job_args_name]
        excution_name = self.name + "_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        job_args = self.args

        args_list = self.phs3.open_object_by_lines(dv.TEMPLATE_BUCKET,
                                                   dv.CLI_VERSION + self.s3_job_path + "/args.properties")

        new_args_list = []
        for arg in args_list:
            if arg.startswith('s3a'):
                arg = arg.replace('s3a:', 's3:')
            new_args_list.append(arg)
        args_dict = write_args(new_args_list, job_args)
        write_data(definition, s3_dag_path, job_name, excution_name, job_args_name_list)

        create_definition = json.dumps(definition)

        step_client = boto3.client('stepfunctions')
        # ???????????????
        step_create_response = step_client.create_state_machine(
            name=self.name + random_num,
            definition=create_definition,
            roleArn=dv.DEFAULT_ROLE_ARN,
            type=dv.DEFAULT_MACHINE_TYPE,
        )
        # ??????cluster_id
        ssm_client = boto3.client('ssm')
        ssm_response = ssm_client.get_parameter(
            Name='cluster_id'
        )
        machine_input = {
            'clusterId': ssm_response['Parameter']['Value']
        }
        ssm_response = ssm_client.get_parameter(
            Name='cluster_id'
        )

        # ???kwargs??????ssm
        ssm_client.put_parameter(
            Name=job_args_name,
            Value=str(args_dict),
            Type='String'
        )

        # ???????????????
        start_response = step_client.start_execution(
            stateMachineArn=step_create_response['stateMachineArn'],
            name=excution_name,
            input=json.dumps(machine_input)
        )

        # ?????????????????????????????? ??????????????????
        execution_response = step_client.list_executions(
            stateMachineArn=step_create_response['stateMachineArn'],
        )

        while execution_response:
            time.sleep(60)
            if len(execution_response['executions']) == 0:
                execution_response = step_client.list_executions(
                    stateMachineArn=step_create_response['stateMachineArn'],
                )
                continue

            execution_response = step_client.list_executions(
                stateMachineArn=step_create_response['stateMachineArn'],
            )
            execution_status = execution_response['executions'][0]['status']
            if execution_status == 'SUCCEEDED':
                step_client.delete_state_machine(
                    stateMachineArn=step_create_response['stateMachineArn']
                )
                break
            if execution_status == 'FAILED':
                step_client.delete_state_machine(
                    stateMachineArn=step_create_response['stateMachineArn']
                )
                raise Exception("Job????????????")
                break

        return 0

    def status(self, **kwargs):
        """
        ???????????????????????????
        """
        self.logger.debug('maxauto ????????? status ??????')
        self.logger.debug(self.__dict__)

