# oc create clusterrole cluster-read-crds --verb=list,get,create --resource=customresourcedefinitions.apiextensions.k8s.io
# oc create role manage-spark --verb=watch --resource=sparkclusters.radanalytics.io,sparkhistoryservers.radanalytics.io
# oc adm policy add-cluster-role-to-user cluster-read-crds system:serviceaccount:spark:spark-operator
# oc policy add-role-to-user manage-spark system:serviceaccount:spark:spark-operator

# oc adm policy add-cluster-role-to-user cluster-admin system:serviceaccount:spark:spark-operator

# oc apply -f manifest/operator-cm.yaml

oc apply -f ../manifest/operator.yaml -n spark
oc apply -f cluster-with-config.yaml -n spark
oc apply -f spark-ui-route.yaml -n spark
oc apply -n spark -f test.spark.application.yaml
oc apply -n spark -f test.spark.application.yaml 