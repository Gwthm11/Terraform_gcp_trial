- We formed two columns for every tickets and also for every workcode_id ,

	- column name : durationA  (duration between transmit time and end time )
	- column name : durationB  (duration between start time  and end time )


- We have found out tickets where work had involved for two consecutive days per ticket .


- We have analysed the tickets with multiple entries and looked for possible combinations .
	-Only two combinations were present ( 1 . [ PT , QH , Project_hourly   ]
							  2 . [ EMLN , QH , Project_hourly ] )


- We also checked the total cost per workcode_id with the invoice and both are matching .
 



















Value
Executive Category
Capacity
Previous Capacity
CUST_ACCT_ID
WTN_NO
ACCT_WTN_CONCAT
In List
Value
Executive Category
Capacity
Previous Capacity
CUST_ACCT_ID
WTN_NO
ACCT_WTN_CONCAT
In List
RESERVEDTN_REQ_TEL_NBR (DTN)
Agreement
Platform
CRNT_GL_CUST_TYPE_CD
Corp Strat LU_CLASS
Inventory Source
Actual Speed
Enabled Speed
BLUE_MARBLE_FLAG
WIRE_CENTER
TOTAL_RECURRING
TOTAL_DISCOUNT
TOTAL_OTHER
TOTAL_TAX_GL
TOTAL_REVENUE
BUNDLE_CODE_1
BUNDLE_DESC_1
BUNDLE_CODE_1_REVENUE
BUNDLE_CODE_2
BUNDLE_DESC_2
BUNDLE_CODE_2_REVENUE
BUNDLE_CODE_3
BUNDLE_DESC_3
BUNDLE_CODE_3_REVENUE
BUNDLE_CODE_4
BUNDLE_DESC_4
BUNDLE_CODE_4_REVENUE
BUNDLE_CODE_5
BUNDLE_DESC_5
BUNDLE_CODE_5_REVENUE
TOTAL_BUNDLE_REVENUE
PRICE_PLAN_1
PRICE_PLAN_1_REVENUE
PRICE_PLAN_2
PRICE_PLAN_2_REVENUE
PRICE_PLAN_3
PRICE_PLAN_3_REVENUE
PRICE_PLAN_4
PRICE_PLAN_4_REVENUE
PRICE_PLAN_5
PRICE_PLAN_5_REVENUE
PRICE_PLAN_6
PRICE_PLAN_6_REVENUE
PRICE_PLAN_7
PRICE_PLAN_7_REVENUE
PRICE_PLAN_8
PRICE_PLAN_8_REVENUE
PRICE_PLAN_9
PRICE_PLAN_9_REVENUE
PRICE_PLAN_10
PRICE_PLAN_10_REVENUE
PRICE_PLAN_11
PRICE_PLAN_11_REVENUE
PRICE_PLAN_12
PRICE_PLAN_12_REVENUE
PRICE_PLAN_13
PRICE_PLAN_13_REVENUE
PRICE_PLAN_14
PRICE_PLAN_14_REVENUE
PRICE_PLAN_15
PRICE_PLAN_15_REVENUE
PRICE_PLAN_16
PRICE_PLAN_16_REVENUE
PRICE_PLAN_17
PRICE_PLAN_17_REVENUE
PRICE_PLAN_18
PRICE_PLAN_18_REVENUE
PRICE_PLAN_19
PRICE_PLAN_19_REVENUE
PRICE_PLAN_20
PRICE_PLAN_20_REVENUE
TOTAL_PRICE_PLAN_REVENUE
TOTAL_BLANK_REVENUE
DISCOUNT_1
DISCOUNT_1_REVENUE
DISCOUNT_2
DISCOUNT_2_REVENUE
DISCOUNT_3
DISCOUNT_3_REVENUE
DISCOUNT_4
DISCOUNT_4_REVENUE
DISCOUNT_5
DISCOUNT_5_REVENUE
DISCOUNT_6
DISCOUNT_6_REVENUE
DISCOUNT_7
DISCOUNT_7_REVENUE
DISCOUNT_8
DISCOUNT_8_REVENUE
TOTAL_DISCOUNT_REVENUE
OTHER_1
OTHER_1_REVENUE
OTHER_2
OTHER_2_REVENUE
OTHER_3
OTHER_3_REVENUE
TOTAL_OTHER_REVENUE
Discounts
Has Discount
Vacation
Status Update
Status Description
Offer Config
Offer









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
