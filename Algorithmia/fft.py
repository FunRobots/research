import Algorithmia

api_key = 'simAkHd6NFelROawvgBT9ouDB6C1'


if __name__ == '__main__':

    photo = open('0.png', 'rb').read()
    print(0)
    client = Algorithmia.client(api_key)
    algo = client.algo('MeisterUrian/FaceFeatures2/0.1.6')
    print(algo.pipe(photo))
