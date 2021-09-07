# Examples from course 

https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide

## Basics

* K8s is a system to deploy containerized applications
* Nodes are individual machines (or VMs) that run containers
* Masters are machines (or VMs) that manage the nodes
* K8s has built images as input, it doesn't build them
* To deploy we update the desired state of master with a config file
and master figures out how to meet the goals.

Each configuration file is used to create an object.

**Controller** objects constantly watch the current state and the desired state,
and figure out the steps to get from one to the other. Example of controllers are:
* **Deployment**
* **Ingress**

### apiVersion
The _api version_ defines the types of objects we can use

Example:
```yaml
apiVersion: v1
```

### metadata

*name* is used to identify the object. When changing a config file,
k8s figures out whether it is a new object or has to update an
existing one from this name property: If an object with the same
name and the same kind already exists it will apply the changes to it.

Example: 
```yaml
metadata:
  name: client-pod
  labels: 
    component: web
```

### kind
The _kind_ refers to the kind of object being created

#### Pod
> Pods are rarely used, more common and flexible is to use
> Deployment objects.

In k8s we don't have containers, we have Pods, which are kind of
a containers' container; we run 1 or more containers inside them.
A Pod is the smallest thing we can deploy

Pods are used to run a container or a set of highly-coupled and dependant containers
that must be deployed and must be running together. Most of the time
a pod will run a single container though. An example of when running
a set of containers inside the same pod; the logger and backup-manager
containers wouldn't make sense without the postgres container

![hello](img/diagrams-14%20-%20why.drawio.png)

Example definition in `client-pod.yml` file
```yaml
kind: Pod
spec:
  containers:
    - name: client
      image: docker-user/image-name
      ports:
        - containerPort: 3000
```

#### Deployment
In practice most of the time *Deployment* objects are used because of the limitations
of configuration updates for pods.

Deployments are meant to manage a set of identical pods. It monitors the state of each
pod and updates/restart them as necessary.

First, specify the version and kind:
```yaml
apiVersion: apps/v1
kind: Deployment
```

Add a name to identify the object
```yaml
metadata:
  name: some-deployment
```

Customize deployment behavior with spec
```yaml
spec:
  replicas: 3  # How many pods will run
  # We have to specify a selector for the deployment to get a reference to the
  # created pods for future updates. Below in template -> metadata -> labels we
  # added the label 'component: web' that we are matching here.
  selector:
    matchLabels:
      component: server
  # Define configuration for the set of pods handled by this deployment config.
  template:
    metadata:
      labels:
        component: server
    spec:
      containers:
         - name: server
           image: stephengrider/multi-server
           ports:
              - containerPort: 5000
```

#### Service

Used to configure networking inside a k8s cluster.

There are four subtypes:
* _ClusterIP_
* _NodePort_
* LoadBalancer
* Ingress

Because Pods are subject to change, their networking is delegated to this Service
object. If we didn't have Service, we would have to manually search for designated
IPs in pods, which are randomly assigned/reassigned in every start/restart of the pod.
Using a Service provides a stable IP:port mapping even though behind the scenes the pod
IP might change.

#### NodePort
Expose a container to the outside world. Only used for dev purposes except few exceptions.

One of the reasons that NodePort is not used in production is because the nodePort
value has to be within the range 30,000-32,767. If not provided, k8s will assign a random
value in that range.

```yaml
kind: Service
spec:
  type: NodePort
  ports:
    - port: 3050        # Open to other pods withing the cluster
      targetPort: 3000  # Redirect incoming traffic to this port inside the pod
      nodePort: 31515   # Open to the outside world, ie: Port to access from the browser
      
  # Select objects using the label-selector system. Refers to the label defined
  # in metadata
  selector:
    component: web
```

#### ClusterIP
Make an object reachable to other objects in the cluster. It does not allow traffic from 
the outside world, just within the cluster.

The name given for this service can be used as a *host name* for reaching out to
this pod. 

```yaml
apiVersion: v1
kind: Service
metadata:
  name: client-cluster-ip-service
spec:
  type: ClusterIP
  selector:
    component: web
  # Same as NodePort, 'port' is the opened port to access this pod from within the
  # cluster, and 'targetPort' is where the traffic is redirected to inside the pod.
  # We don't have a 'nodePort' though because ClusterIP only allows inter-cluster
  # traffic.
  ports:
    - port: 3050
      targetPort:  3000
```

#### Ingress
Expose a set of services to the outside world. This a controller-type object: it takes a 
desired state and figures out the steps to get there. 
For an ingress object, the desired state will include a set of routing rules. This set of
rules will be fed into kubectl which will create an ingress-controller. This controller
will make our rules a reality somehow, some-thing that will accept incoming traffic.

*ingress-nginx*  [docs](https://kubernetes.github.io/ingress-nginx/)
ingress-nginx will have a different config depending on the environment (local, aws, gc,
etc.)



#### LoadBalancer
Legacy way of allowing traffic into one set of pods


## kubectl

cli to interact with k8s

#### Apply configuration file
```shell
# kubectl apply -f <config-file>|<config-folder>
kubectl apply -f examples/1-simplek8s/client-pod.yml  # apply single file
kubectl apply -f examples/2-complex/k8s               # apply all files in folder 
```

#### Remove an object
```shell
# kubectl delete -f <config-file>
kubectl delete -f examples/1-simplek8s/client-pod.yml
```

#### Get running objects
```shell
# kubectl get <object-type>

kubectl get pods
kubectl get services
kubectl get deployments
```

```shell
$ kubectl get pods -o wide
NAME                                 READY   STATUS    RESTARTS   AGE     IP          NODE             NOMINATED NODE   READINESS GATES
client-deployment-7cb6c958f7-7zctf   1/1     Running   0          4m45s   10.1.0.83   docker-desktop   <none>           <none>

# IP is the internal Pod IP inside the Node
```

#### Get info about a running object
```shell
# kubectl describe <object-type> [<object-name>]
kubectl describe pod client-pod
```

## Development flow

1. Update the code
2. Rebuild and push the image
3. Recreate our pods with new image


### Recreate our pods with new image
*Problem:* Lets say we have a deployment configuration that uses 
```yaml
...
    spec:
        containers:
        - name: client
          image: stephengrider/multi-client
```
When we make a change and rebuild the image, we will still be using the same image
tag (:latest by default). How do we update the Pods to use this latest image? If we
try to re-apply using `kubectl apply -f <my-deployment-file>`, k8s will do nothing
because there are no changes in the config file.

*Solution:* 
1. Tag the image with a version number
   1. For example run `docker build -t stephengrider/multi-client:v5 .`
   2. `docker push stephengrider/multi-client:v5`
2. Use an imperative command to force an update of the image version used.
   1. `kubectl set image deployment/client-deployment client=stephengrider/multi-client:v5`

## Persistence

There are 3 data store mechanisms in k8s:
1. Volume
2. Persistent Volume
3. Persistent Volume Claim

### Volume
**Important**: A *Volume* in k8s **is not the same as a Docker Volume**.
In k8s, a Volume is a data store that is **tied to a specific Pod**. That means that
if the Pod dies, then the Volume data is lost. (The Volume data survives containers 
restarts, but not Pod restarts)

### Persistent Volume
A persistent volume outlives the Pod. If the pod is killed/restarted, then the persistent
volume's data is preserved. 

### Persistent Volume Claim
A PVC is analogous to a catalogue of persistent volumes: we configure the options 
available inside a cluster. Then a Pod will request to use one of these options. 
When a Pod requests one Persistent Volume 1 of two things can happen:
1. The PV was already created: *Statically provisioned Persistent Volume*
2. The PV wasn't yet created and K8s will dynamically create one: *Dynamically 
provisioned persistent volume*

So a PVC is not an actual Persistent Volume, but a sort of catalogue of those from
which the Pods can choose. K8s is responsible for either finding an already created
PV with the defined config, or dynamically create one.

#### Config
Example PVC configuration:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: database-persistent-volume-claim
# Here we are advertising an option to be used by the pods. K8s is responsible to 
# either find or create a PV with these spec. We are not creating anything, 
# just defining the "catalogue" options
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

Then, to use this configuration in a Deployment:
```yaml
kind: Deployment
...
spec:
  template:
    # ...
    spec:
      # Allocate a persistent volume defined in the claim
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: database-persistent-volume-claim
      containers:
          # ...
          # Ask the container to use one of the allocated volumes
          volumeMounts:
            - name: postgres-storage  # Refer to the allocated volume
              mountPath: /var/lib/postgresql/data
              # inside the Volume, store postgres data in a 'postgres' directory.
              # Don't know why, but use this to make postgres volume work.
              subPath: postgres
```

*accessModes*: We have three types of accessModes:
1. ReadWriteOnce: *A single node* can read and write
2. ReadOnlyMany: *Many nodes* can only read
3. ReadWriteMany: *Many nodes*  can read and write


## Environment Variables
Env variables can be added in the Deployment definition:

```yaml
# ...
spec:
  template:
    spec:
      env:
        - name: MYENVVAR
          value: MYENVVAR_VALUE
```

### secrets
To store sensitive information such as passwords we can use Secrets object. To create
this object we have to run an imperative command (we don't create a config file like the
other objects) which means we have to run this command both locally for development
and in production.

Command:
```shell
# kubectl create secret <secret-type> <secret-name> --from-literal key=value
kubectl create secret generic pgpassword --from-literal PGPASSWORD=password123
```

*secret-type*:
1. generic: arbitrary key-value pairs
2. docker-registry: authentication for a private docker registry
3. tls: https setup

_secret-name_: used to consume the secret later on

List secrets: `kubectl get secrets`

#### Consuming secrets
To consume the above generated secret we have to add the following into the environment
variables definition:
```yaml
# ...
env:
   - name: PGPASSWORD
     valueFrom:
       secretKeyRef:
         name: pgpassword
         key: PGPASSWORD
```


### Dashboard
See https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/learn/lecture/15492160#questions

