import boto3

s3 = boto3.resource('s3')
client = boto3.client('rekognition')
response=client.create_collection(CollectionId='miamiheatfaces')


def lista_imagens():
    imagens=[]
    bucket = s3.Bucket('fa-imagens-enrico')
    for imagem in bucket.objects.all():
        imagens.append(imagem.key)
    print(imagens)
    return imagens

def indexa_colecao(imagens):
    for i in imagens:
        response=client.index_faces(
            CollectionId='miamiheatfaces',
            DetectionAttributes=[
            ],
            ExternalImageId=i[:-4],
            Image={
                'S3Object': {
                    'Bucket': 'fa-imagens-enrico',
                    'Name': i,
                },
            },

        )

imagens = lista_imagens()
indexa_colecao(imagens)