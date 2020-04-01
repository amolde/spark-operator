# oc create clusterrole cluster-read-crds --verb=list,get,create --resource=customresourcedefinitions.apiextensions.k8s.io
# oc create role manage-spark --verb=watch --resource=sparkclusters.radanalytics.io,sparkhistoryservers.radanalytics.io
# oc adm policy add-cluster-role-to-user cluster-read-crds system:serviceaccount:spark:spark-operator
# oc policy add-role-to-user manage-spark system:serviceaccount:spark:spark-operator
oc adm policy add-cluster-role-to-user cluster-admin system:serviceaccount:spark:spark-operator