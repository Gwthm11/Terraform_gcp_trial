






import multiprocessing
import time
   
  
def square(x):
    return x * x
   
if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=4)
    inputs = [0,1,2,3,4]
    outputs = pool.map(square, inputs)
    print("Input: {}".format(inputs))
    print("Output: {}".format(outputs))















def ms_teams_alert(context, teams_webhook=webhook):
	dag_id = context[“dag_run”].dag_id
	task_id = context[“task_instance”].task_id
	context[“task_instance”].xcom_push(key=dag_id, value=True)
	logs_url = context.get(“task_instance”).log_url
	teams_notification = pymsteams.connectorcard(teams_webhook)
	message = “`{}` has failed on task: `{}`”.format(dag_id, task_id)
	teams_notification.title(“ERROR ALERT !!”)
	teams_notification.color(“red”)
	teams_notification.text(“ERROR MESSAGE: “ + message)
	teams_notification.addLinkButton(“LOG URL”, logs_url)
	teams_notification.send()



;WITH CTE AS (
    SELECT * ,
        RN = ROW_NUMBER() OVER (ORDER BY [count] DESC)
    FROM T1
)
,CTE2 AS (
    SELECT *, 
        RN2 = ROW_NUMBER() OVER(ORDER BY CEILING( RN / 5.00 ), (( 1 - CEILING( RN / 5.00 )) * [COUNT] ) DESC ) 
    FROM CTE 
)
SELECT 
    CTE2.rid, 
    CTE2.[count], 
    ((RN2+1)%5) +1 GroupIndex, 
    SUM(CTE2.[count]) OVER (PARTITION BY ((RN2+1)%5)) CmlTotal 
FROM CTE2





















from google.cloud import bigquery

client = bigquery.Client()

datasets = list(client.list_datasets())
project = client.project

if datasets:
    print('Datasets in project {}:'.format(project))
    for dataset in datasets:  # API request(s)
        print('Dataset: {}'.format(dataset.dataset_id))

        query_job = client.query("select table_id, sum(size_bytes)/pow(10,9) as size from `"+dataset.dataset_id+"`.__TABLES__ group by 1")

        results = query_job.result()
        for row in results:
            print("\tTable: {} : {}".format(row.table_id, row.size))

else:
    print('{} project does not contain any datasets.'.format(project))
















DECLARE gb_divisor INT64 DEFAULT 1024*1024*1024;
DECLARE tb_divisor INT64 DEFAULT gb_divisor*1024;
DECLARE cost_per_tb_in_dollar INT64 DEFAULT 5;
DECLARE cost_factor FLOAT64 DEFAULT cost_per_tb_in_dollar / tb_divisor;

SELECT
 ROUND(SUM(total_bytes_processed) / gb_divisor,2) as bytes_processed_in_gb,
 ROUND(SUM(IF(cache_hit != true, total_bytes_processed, 0)) * cost_factor,4) as cost_in_dollar,
 user_email,
FROM (
  (SELECT * FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_USER)
  UNION ALL
  (SELECT * FROM `other-project.region-us`.INFORMATION_SCHEMA.JOBS_BY_USER)
)
WHERE
  DATE(creation_time) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) and CURRENT_DATE()
GROUP BY 








pip list | tail -n +3 | awk '{print $1}' | xargs pip show | grep -E 'Location:|Name:' | cut -d ' ' -f 2 | paste -d ' ' - - | awk '{print $2 "/" tolower($1)}' | xargs du -sh 2> /dev/null | sort -hr
du -a /etc/ | sort -n -r | head -n 10

df = df_first.set_index('EmpID').combine_first(df_second.set_index('EmpID')).reset_index()
print (df)
























from bs4 import BeautifulSoup
import dask, requests, time
import pandas as pd

base_url = 'https://www.lider.cl/supermercado/category/Despensa/?No={}&isNavRequest=Yes&Nrpp=40&page={}'

def scrape(id):
    page = id+1; start = 40*page
    bs = BeautifulSoup(requests.get(base_url.format(start,page)).text,'lxml')
    prods = [prod.text for prod in bs.find_all('span',attrs={'class':'product-description js-ellipsis'})]
    prods = [prod.text for prod in prods]
    brands = [b.text for b in bs.find_all('span',attrs={'class':'product-name'})]

    sdf = pd.DataFrame({'product': prods, 'brand': brands})
    return sdf

data = [dask.delayed(scrape)(id) for id in range(10)]
df = dask.delayed(pd.concat)(data)
df = df.compute()

import aiohttp
import asyncio
import requests
import time

from key import key

start_time = time.time()

channel_id = 'UC-QDfvrRIDB6F0bIO4I4HkQ'

url = f'https://www.googleapis.com/youtube/v3/channels?id={channel_id}&key={key}&part=contentDetails'
r = requests.get(url)
results = r.json()['items']


playlist_id = results[0]['contentDetails']['relatedPlaylists']['uploads']

url = f'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&key={key}&part=contentDetails&maxResults=50'

video_ids = []
while True:
    r = requests.get(url)
    results = r.json()
    if 'nextPageToken' in results:
        nextPageToken = results['nextPageToken']
    else:
        nextPageToken = None

    if 'items' in results:
        for item in results['items']:
            videoId = item['contentDetails']['videoId']
            video_ids.append(videoId)

    if nextPageToken:
        url = f'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&pageToken={nextPageToken}&key={key}&part=contentDetails&maxResults=50'
    else:
        break



'''
view_counts = []
for video_id in video_ids:
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={key}&part=statistics'
    r = requests.get(url)
    results = r.json()['items']
    viewCount = results[0]['statistics']['viewCount']
    view_counts.append(int(viewCount))
print('Number of videos:', len(view_counts))
print('Average number of views:', sum(view_counts) / len(view_counts))
'''

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for video_id in video_ids:
            task = asyncio.ensure_future(get_video_data(session, video_id))
            tasks.append(task)

        view_counts = await asyncio.gather(*tasks)

    print('Number of videos:', len(view_counts))
    print('Average number of views:', sum(view_counts) / len(view_counts))

async def get_video_data(session, video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={key}&part=statistics'

    async with session.get(url) as response:
        result_data = await response.json()
        results = result_data['items']
        viewCount = results[0]['statistics']['viewCount']
        return int(viewCount)

asyncio.run(main())

print("--- %s seconds ---" % (time.time() - start_time))




from airflow import models
from airflow.operators.bash_operator import BashOperator
from airflow.providers.google.cloud.operators.kubernetes_engine import (
    GKECreateClusterOperator,
    GKEDeleteClusterOperator,
    GKEStartPodOperator,
)
from airflow.utils.dates import days_ago


with models.DAG(
    "example_gcp_gke",
    schedule_interval=None,  # Override to match your needs
    start_date=days_ago(1),
    tags=["example"],
) as dag:

    # TODO(developer): update with your values
    PROJECT_ID = "my-project-id"
    CLUSTER_ZONE = "us-west1-a"
    CLUSTER_NAME = "example-cluster"
    CLUSTER = {"name": CLUSTER_NAME, "initial_node_count": 1}
    create_cluster = GKECreateClusterOperator(
        task_id="create_cluster",
        project_id=PROJECT_ID,
        location=CLUSTER_ZONE,
        body=CLUSTER,
    )
    # Using the BashOperator to create node pools is a workaround
    # In Airflow 2, because of https://github.com/apache/airflow/pull/17820
    # Node pool creation can be done using the GKECreateClusterOperator

    create_node_pools = BashOperator(
        task_id="create_node_pools",
        bash_command=f"gcloud container node-pools create pool-0 \
                        --cluster {CLUSTER_NAME} \
                        --num-nodes 1 \
                        --zone {CLUSTER_ZONE} \
                        && gcloud container node-pools create pool-1 \
                        --cluster {CLUSTER_NAME} \
                        --num-nodes 1 \
                        --zone {CLUSTER_ZONE}",
    )

    kubernetes_min_pod = GKEStartPodOperator(
        # The ID specified for the task.
        task_id="pod-ex-minimum",
        # Name of task you want to run, used to generate Pod ID.
        name="pod-ex-minimum",
        project_id=PROJECT_ID,
        location=CLUSTER_ZONE,
        cluster_name=CLUSTER_NAME,
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=["echo"],
        # The namespace to run within Kubernetes, default namespace is
        # `default`.
        namespace="default",
        # Docker image specified. Defaults to hub.docker.com, but any fully
        # qualified URLs will point to a custom repository. Supports private
        # gcr.io images if the Composer Environment is under the same
        # project-id as the gcr.io images and the service account that Composer
        # uses has permission to access the Google Container Registry
        # (the default service account has permission)
        image="gcr.io/gcp-runtimes/ubuntu_18_0_4",
    )

    kubenetes_template_ex = GKEStartPodOperator(
        task_id="ex-kube-templates",
        name="ex-kube-templates",
        project_id=PROJECT_ID,
        location=CLUSTER_ZONE,
        cluster_name=CLUSTER_NAME,
        namespace="default",
        image="bash",
        # All parameters below are able to be templated with jinja -- cmds,
        # arguments, env_vars, and config_file. For more information visit:
        # https://airflow.apache.org/docs/apache-airflow/stable/macros-ref.html
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=["echo"],
        # DS in jinja is the execution date as YYYY-MM-DD, this docker image
        # will echo the execution date. Arguments to the entrypoint. The docker
        # image's CMD is used if this is not provided. The arguments parameter
        # is templated.
        arguments=["{{ ds }}"],
        # The var template variable allows you to access variables defined in
        # Airflow UI. In this case we are getting the value of my_value and
        # setting the environment variable `MY_VALUE`. The pod will fail if
        # `my_value` is not set in the Airflow UI.
        env_vars={"MY_VALUE": "{{ var.value.my_value }}"},
    )

    kubernetes_affinity_ex = GKEStartPodOperator(
        task_id="ex-pod-affinity",
        project_id=PROJECT_ID,
        location=CLUSTER_ZONE,
        cluster_name=CLUSTER_NAME,
        name="ex-pod-affinity",
        namespace="default",
        image="perl",
        cmds=["perl"],
        arguments=["-Mbignum=bpi", "-wle", "print bpi(2000)"],
        # affinity allows you to constrain which nodes your pod is eligible to
        # be scheduled on, based on labels on the node. In this case, if the
        # label 'cloud.google.com/gke-nodepool' with value
        # 'nodepool-label-value' or 'nodepool-label-value2' is not found on any
        # nodes, it will fail to schedule.
        affinity={
            "nodeAffinity": {
                # requiredDuringSchedulingIgnoredDuringExecution means in order
                # for a pod to be scheduled on a node, the node must have the
                # specified labels. However, if labels on a node change at
                # runtime such that the affinity rules on a pod are no longer
                # met, the pod will still continue to run on the node.
                "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [
                        {
                            "matchExpressions": [
                                {
                                    # When nodepools are created in Google Kubernetes
                                    # Engine, the nodes inside of that nodepool are
                                    # automatically assigned the label
                                    # 'cloud.google.com/gke-nodepool' with the value of
                                    # the nodepool's name.
                                    "key": "cloud.google.com/gke-nodepool",
                                    "operator": "In",
                                    # The label key's value that pods can be scheduled
                                    # on.
                                    "values": [
                                        "pool-1",
                                    ],
                                }
                            ]
                        }
                    ]
                }
            }
        },
    )
    kubernetes_full_pod = GKEStartPodOperator(
        task_id="ex-all-configs",
        name="full",
        project_id=PROJECT_ID,
        location=CLUSTER_ZONE,
        cluster_name=CLUSTER_NAME,
        namespace="default",
        image="perl",
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=["perl"],
        # Arguments to the entrypoint. The docker image's CMD is used if this
        # is not provided. The arguments parameter is templated.
        arguments=["-Mbignum=bpi", "-wle", "print bpi(2000)"],
        # The secrets to pass to Pod, the Pod will fail to create if the
        # secrets you specify in a Secret object do not exist in Kubernetes.
        secrets=[],
        # Labels to apply to the Pod.
        labels={"pod-label": "label-name"},
        # Timeout to start up the Pod, default is 120.
        startup_timeout_seconds=120,
        # The environment variables to be initialized in the container
        # env_vars are templated.
        env_vars={"EXAMPLE_VAR": "/example/value"},
        # If true, logs stdout output of container. Defaults to True.
        get_logs=True,
        # Determines when to pull a fresh image, if 'IfNotPresent' will cause
        # the Kubelet to skip pulling an image if it already exists. If you
        # want to always pull a new image, set it to 'Always'.
        image_pull_policy="Always",
        # Annotations are non-identifying metadata you can attach to the Pod.
        # Can be a large range of data, and can include characters that are not
        # permitted by labels.
        annotations={"key1": "value1"},
        # Resource specifications for Pod, this will allow you to set both cpu
        # and memory limits and requirements.
        # Prior to Airflow 1.10.4, resource specifications were
        # passed as a Pod Resources Class object,
        # If using this example on a version of Airflow prior to 1.10.4,
        # import the "pod" package from airflow.contrib.kubernetes and use
        # resources = pod.Resources() instead passing a dict
        # For more info see:
        # https://github.com/apache/airflow/pull/4551
        resources={"limit_memory": "250M", "limit_cpu": "100m"},
        # If true, the content of /airflow/xcom/return.json from container will
        # also be pushed to an XCom when the container ends.
        do_xcom_push=False,
        # List of Volume objects to pass to the Pod.
        volumes=[],
        # List of VolumeMount objects to pass to the Pod.
        volume_mounts=[],
        # Affinity determines which nodes the Pod can run on based on the
        # config. For more information see:
        # https://kubernetes.io/docs/concepts/configuration/assign-pod-node/
        affinity={},
    )
    delete_cluster = GKEDeleteClusterOperator(
        task_id="delete_cluster",
        name=CLUSTER_NAME,
        project_id=PROJECT_ID,
        location=CLUSTER_ZONE,
    )

    create_cluster >> create_node_pools >> kubernetes_min_pod >> delete_cluster
    create_cluster >> create_node_pools >> kubernetes_full_pod >> delete_cluster
    create_cluster >> create_node_pools >> kubernetes_affinity_ex >> delete_cluster
    create_cluster >> create_node_pools >> kubenetes_template_ex >> delete_cluster

    
https://download.oracle.com/otn_software/linux/instantclient/215000/oracle-instantclient-basic-21.5.0.0.0-1.el8.x86_64.rpm  
https://download.oracle.com/otn_software/linux/instantclient/215000/oracle-instantclient-devel-21.5.0.0.0-1.el8.x86_64.rpm
https://docs.databricks.com/_static/notebooks/mlflow/mlflow-end-to-end-example.html
