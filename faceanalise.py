import boto3
import json

client = boto3.client('rekognition')
s3 = boto3.resource('s3')

def list_collections():
    max_results = 10

    print('Printing Collections')
    response = client.list_collections(MaxResults=max_results)
    collection_count = 0
    done = False
    collectionsList = []

    while done == False:
        collections = response['CollectionIds']

        for collection in collections:
            print(collection)
            collection_count += 1
        if 'NextToken' in response:
            nextToken = response['NextToken']
            response = client.list_collections(NextToken=nextToken, MaxResults=max_results)
        else:
            done = True

    return collection_count


def detecta_faces():
    faces_detectadas = client.index_faces(
        CollectionId='miamiheatfaces',
        DetectionAttributes=['DEFAULT'],
        ExternalImageId='TEMPORARIA',
        Image={
            'S3Object': {
                'Bucket': 'fa-imagens-enrico',
                'Name': '_analise.png',
            },

        },
    )
    return faces_detectadas


def cria_lista_faceId_detectadas(faces_detectadas):
    faceId_detectadas = []
    for i in range(len(faces_detectadas['FaceRecords'])):
        faceId_detectadas.append(faces_detectadas['FaceRecords'][i]['Face']['FaceId'])
    return faceId_detectadas


def compara_imagens(faceId_detectadas):
    resultado_comparacao = []
    for ids in faceId_detectadas:
        resultado_comparacao.append(
            client.search_faces(
                CollectionId='miamiheatfaces',
                FaceId=ids,
                FaceMatchThreshold=80,
                MaxFaces=10,
            )
        )
    return resultado_comparacao


def gera_dados_json(resultado_comparacao):
    dados_json = []
    for face_matches in resultado_comparacao:
        if (len(face_matches.get('FaceMatches'))) >= 1:
            perfil = dict(nome=face_matches['FaceMatches'][0]['Face']['ExternalImageId'],
                          faceMatch=round(face_matches['FaceMatches'][0]['Similarity'], 2))
            print(perfil)
            dados_json.append(perfil)

    return dados_json


def publica_dados(dados_json):
    arquivo = s3.Object('fa-site-enrico', 'dados.json')
    arquivo.put(Body=json.dumps(dados_json))


def exclui_imagem_colecao(faceId_detectadas):
    client.delete_faces(
        CollectionId='miamiheatfaces',
        FaceIds=faceId_detectadas,
    )

faces_detectadas = detecta_faces()
faceId_detectadas = cria_lista_faceId_detectadas(faces_detectadas)
resultado_comparacao = compara_imagens(faceId_detectadas)
dados_json = gera_dados_json(resultado_comparacao)
publica_dados(dados_json)
exclui_imagem_colecao(faceId_detectadas)
print(json.dumps(dados_json, indent=4))