import boto3

client = boto3.client('rekognition')
s3  =   boto3.resource('s3')


def deleta_face(collection_id, faces):
    response=client.delete_faces(CollectionId=collection_id,
                                 FaceIds=faces)

    print(str(len(response['DeletedFaces'])) + ' faces deleted:')
    for faceId in response['DeletedFaces']:
        print(faceId)
    return len(response['DeletedFaces'])

def lista_faces(collection_id):

    maxResults = 10
    faces_count = 0
    tokens = True

    response = client.list_faces(CollectionId=collection_id,
                                 MaxResults=maxResults)

    print('Faces in collection ' + collection_id)
    todas_faces_id =  []
    while tokens:

        faces = response['Faces']

        for face in faces:
            print(face['FaceId'])
            todas_faces_id.append(face['FaceId'])
            faces_count += 1
        if 'NextToken' in response:
            nextToken = response['NextToken']
            response = client.list_faces(CollectionId=collection_id,
                                         NextToken=nextToken, MaxResults=maxResults)
        else:
            tokens = False
    return todas_faces_id

collection = 'miamiheat'

faces = lista_faces(collection)
print(faces)
#deleta_face(collection, faces)