import boto3

s3 = boto3.client('s3')
bucket_name = "advizo-iot-fire-resources"
folders = ["athenadb/input/production_raw_iot_advizo/map_factory"]

def create_folder(folder_name,client,bucket):
    for folder in folder_name:
      response = client.list_objects_v2(Bucket=bucket, Prefix=folder+'/')
      if 'Contents' in response:
          print(f"Folder {folder} already exists [create_folder]")
      else:
          print(f"Creating folder {folder} [create_folder]")                             
          client.put_object(Bucket=bucket_name, Key=(folder+'/'))

def main():
    create_folder(folders,s3,bucket_name)

if __name__ == "__main__":
    main()