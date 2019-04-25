### Build docker image and push to registry

```bash
$ docker build -t whereisqa .
$ docker run -it -p 8080:8080 whereisqa
$ docker tag whereisqa:latest 457398059321.dkr.ecr.us-east-1.amazonaws.com/whereisqa:latest
$ $(aws ecr get-login --no-include-email --region us-east-1)
$ docker push 457398059321.dkr.ecr.us-east-1.amazonaws.com/whereisqa:latest
```

When running locally do not forget to mount either source code or `config_local.py` file or
just pass required environment variables when launching container

```bash
$ docker run -it -v $(pwd):/opt/app -p 8080:8080 whereisqa
```

### Running on Kubernetes

```bash
$ minikube start --vm-driver=hyperkit
$ minikube dashboard
$ kubectl config get-contexts
$ kubectl config use-context minikube
```

Enable pulling containers from AWS

```bash
$ minikube addons configure registry-creds
$ minikube addons enable registry-creds
```

Create secrets

```bash
$ kubectl apply -f kubernetes/secret.yml
$ kubectl get secrets
```

Create deployment

```bash
$ kubectl create -f kubernetes/app-deployment.yml
$ kubectl get deployments
```

Create service

```bash
$ kubectl create -f kubernetes/app-service.yml
$ kubectl get pods
```

Add ingress for a service

```bash
$ 

```

Check app is running

```bash
$ kubectl get services
$ echo $(minikube ip)
$ minikube service whereisqa --url
```

and visit the url provided.

### Scaling

Launch more replicas for specific deployment

```bash
$ kubectl scale --replicas=3 deployment whereisqa
```

Scale down to 1 replica

```bash
$ kubectl scale --replicas=1 deployment whereisqa
```

### Deploying new version of the code

Set a new image to use and confirm successful rollout 

```bash
$ kubectl set image deployments/whereisqa whereisqa=457398059321.dkr.ecr.us-east-1.amazonaws.com/whereisqa:v2
$ kubectl rollout status deployments/whereisqa
deployment "whereisqa" successfully rolled out
```

Check pods and make sure they use new updated image

```bash
$ kubectl get pods
$ kubectl describe pods | grep -i image
```

To perform a [rollback](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment) 
to the previous version

```bash
$ kubectl rollout undo deployments/whereisqa
deployment.extensions/whereisqa rolled back
```

If you want to be reverted to some specific revision 
```bash
$ kubectl rollout history deployment/whereisqa
$ kubectl rollout undo deployment/whereisqa --to-revision=2
```

### Troubleshooting

* `Waiting for SSH access...` takes too long

```bash
$ rm -f ~/.minikube/machines/minikube/hyperkit.pid
```

* `botocore.exceptions.ClientError: An error occurred (AuthFailure) when calling the DescribeInstances operation: AWS was not able to validate the provided access credentials`

Restart docker machine first and then restart minikube (issue with clock sync)

```bash
$ minikube stop
$ minikube start
```
