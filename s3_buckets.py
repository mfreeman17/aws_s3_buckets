import boto3
import math


access_key = str(input("Enter AWS Access Key: "))
secret_access_key= str(input("Enter AWS Secret Access Key: "))


def ask_byte_mode():
    print("How do you want the files sizes to be displayed?: \n"
          "1) Bytes \n"
          "2) kB  \n"
          "3) MB \n"
          "4) GB \n")

    byte_mode = int(input("Enter the number to select: "))
    return byte_mode

byte_mode = ask_byte_mode()
while (byte_mode<1 or byte_mode>4):
    print("please select a valid number")
    byte_mode= ask_byte_mode()

def display_size(byte_length):
    asf = "Aggregate size of files: "
    if(byte_mode==1):
        print(asf, byte_length, " B")
    elif(byte_mode==2):
        print(asf, byte_length/1024 , " kB")
    elif(byte_mode==3):
        print(asf, byte_length/(math.pow(1024,2)), " MB")
    elif(byte_mode==4):
        print(asf, byte_length/math.pow(1024,3), " GB")


s3 = boto3.resource(
    service_name='s3',
    aws_access_key_id= access_key,
    aws_secret_access_key= secret_access_key)

for bucket in s3.buckets.all():
    print("Bucket Name: ", bucket.name)
    print("Creation Date: ", bucket.creation_date)
    bucket_size=0
    num_objects=0
    most_recent = bucket.creation_date     #most recent object is set to bucket creation date at first (this will be oldest possible modified date for files)
    for object in bucket.objects.all():
        bucket_size+=object.size
        num_objects+=1
        most_recent= max(most_recent,object.last_modified) #the max of the most_recent and current object last modified will be new most recent file
    print("Number of files: ", num_objects)
    display_size(bucket_size)
    print("Last modified date of the most recent file: ", most_recent) 
    print("----------------------------------------------------------------")
