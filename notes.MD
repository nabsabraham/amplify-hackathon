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


--- 

Store Operations 
Mike Doucette,

focal = digital shelf 
manual operations in store 
our compeittors are doing this - 
longevity, purchasing and supply chain to make sure products get out the door

what are your suggestions about getting this in store
innovation team has projects that get cameras in the store
automate decision making in the store is to point a camera at it

igor's team - we don't have this camera data and we try to proxy it 
knowing how many people are in the store is actually really useful 

using mac addresses and bluetooth to get phones to ping out

talk to Dina about some of the work she's had to do 

Paul's consumer behavior - Igor

monetize on customer behaviour 
LCBO has a lab in Waterloo 

costs will be as follows: 
store operations - how to have them in stores, mounting, physical attributes
business = activities taken for thecost of profit 

find out what it would cost to sell through baabns before it goes bad 
if we could justify the offset of the cost with one product in a store with a sell-through
* just to pay for this exercise, selling at a rate of x, this many items
2. now, WE HAVE CAMERAS IN THE STORE THAT ARE TIED TO US - maintenance of the cameras , operations cost
so what else can we do 00 ancillary benefits
now we have the opportunity to tie some stuff into this 
additional revenue opportunities beyond this 
we estimate there would be more profitability 

scalability is an operational cost that will come out of the research
getting data in the cloud is infinitely scalable 
how high res do we have to go -- does it have the ability to filter out certain bandwidths of light?



mike.doucette@loblaw.ca


--- 
check in with Mike Doucette
what is the store operation cost? what is the manentnance cost for camera?how many cameras do we need?

for one product for example banana, does he have any number for spoilage?

what will be the impact of this on business from Mike perspective?
in terms of scalibity, how w can have efficiency in the operation?


--- 
automating the image
the cost component 

300 images, 24 pics 
capital cost: hardware cost is next to nothing
opex cost: is next to nothing (5k) 
s
well how would this solution work with a fixed shelf camera solution? 
how would a solution like that integrat e with this? 

vendor cost: 250k 
integrating with loblaw system: 4-500k for a 6 month period 

what would differentiate a technology like this? 
being flexible for a solution that is just for fresh because we don't have that yet 
produce and frozen food is a challenge

is it true that we always keep this specific produce in the center of the store? 
for market/discount, it is similar 
you wont find fresh in the center of the store

market = zehrs, loblaws (gta) 
discount = no frills, superstore

where do we typically keep the produce in the store 

500k to a million for a couple stores


