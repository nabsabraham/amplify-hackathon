start with datastore
blob storage = S3 = gcp bucket
dataset is a particular table
ten node cluster where each node is a computer and each computer can have X number of cores

azure/MachineLearningNotebooks

how to add logic to the powerapps front end? 
how to read from a db? 
transfer learning for images and labelling
you need a storage blob i think 


how to write from cognitive services to database


should we even use cognitive services? It doesnt seem like we can just use our custom model!
if no - what do we use? how to connect to powerapps?

what's ML studio versus just machine learning? 


- if we predict a produce is in class 2, we're going to say that's like spoils in 2 days
- CV engine: 
	- first option: containerize the model and dependencies deploy that to AzureContainerInstance
		- https://docs.microsoft.com/en-us/azure/machine-learning/tutorial-deploy-models-with-aml
		- https://github.com/Azure/MachineLearningNotebooks/

	- this is a docker image that 
	- second option: keep it as a flask application
	- third option: load the model into python and save it as csv, batch fashion 

For connection: 
	- Take image, convert to bytes
	- ask Will for PowerApps connection
		- hey i have an API with json and logic 
		- 
	Recommendation part:	
	- dump the recipes into a csv
	- 


Hossein: 

predict spoilage for all products
dump output into csv - provision blob storage
	- make that open 
	- create a storage account and make it general purpose
	- https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
	- private option means people have to have some auth to get into it 
	- python script will read the csv, find out which recipes to recommend
	- pd.read_csv('public_url_to_blog_storage')

https://docs.microsoft.com/en-us/python/api/overview/azure/storage-blob-readme?view=azure-python

invite anyone to the subscription
- https://blog.atwork.at/post/Invite-external-users-to-your-Azure-subscription



use ACI for demo purposes

1 hour -> 11-12 
