import argparse
from mlearn.clustering import kmeans 

if __name__ == '__main__':
    """ Example: patrick@Beatrice:~/projects/machine_learning$ python run_kmeans.py mlearn.data.iris 3 100 """
    parser = argparse.ArgumentParser(description='Run k-means clustering')
    parser.add_argument('module', type=str, help='data module')
    parser.add_argument('k', type=int, help='number of clusters')
    parser.add_argument('max_iterations', type=int,
            help='maximum number of iterations')
    args = parser.parse_args()
    kmeans = kmeans.Kmeans(args.module, args.k, args.max_iterations)
    kmeans.run()
