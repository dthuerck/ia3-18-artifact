import argparse
import os
import json

# define CLI interface
aparser = argparse.ArgumentParser(description='Artifact runner for our IA3 2018 paper.')
aparser.add_argument('mode', action='store', choices=['setup', 'clean', 'replicate', 'solve', 'stats'])
aparser.add_argument('--matrix', '-s', action='store', default='boyd1', required=False)
aparser.add_argument('--precision', '-p', action='store', type=int, default=1, required=False) 
aparser.add_argument('--pivot_method', '-m', action='store', type=int, default=2, required=False)
aparser.add_argument('--fill_level', '-l', action='store', type=int, default=0, required=False)
aparser.add_argument('--fill_factor', '-f', action='store', type=float, default=8.0, required=False)
aparser.add_argument('--threshold', '-t', action='store', type=float, default=1e-4, required=False)
aparser.add_argument('--max_level', '-x', action='store', type=int, default=5, required=False)

args = aparser.parse_args()

# working dir
cwd = os.getcwd()

# create folder share/ if not there
os.system('mkdir -p ' + cwd + '/share')

# load IA3 parameter file
with open(cwd + '/params/ia3_data.json', 'r') as f:
    ia3_params = json.load(f)

# switch modes
if(args.mode == 'setup'):
    print('Setting up docker container... Please wait until docker reports done (takes a while!)!')

    docker_path = cwd + '/' + 'container'
    os.system('docker build -t culip:ia3-18-artifact ' + docker_path)

elif(args.mode == 'clean'):
    print('Removing docker container...')

    os.system('docker image rm -f culip:ia3-18-artifact')

elif(args.mode == 'replicate'):
    print('Replicating experiment with matrix %s...' % args.matrix);

    if not args.matrix in ia3_params.keys():
        print('Matrix %s is not part of the IA3 2018 test set, exiting...' % args.matrix)

    base_path = '/culip/data/' + args.matrix
    matrix_path = base_path + '/matrix.mtx'
    perm_path = base_path + '/perm.mtx'
    blks_path = base_path + '/blks.mtx'
    pivs_path = base_path + '/pivs.mtx'
    cmdline = './culip-block-ildlt %s %s %s %s %d %d %d %f %f' % (matrix_path, perm_path, blks_path, pivs_path, \
        ia3_params[args.matrix]['precision'], ia3_params[args.matrix]['pivot_method'], \
	    ia3_params[args.matrix]['fill_level'], ia3_params[args.matrix]['fill_factor'], \
	    ia3_params[args.matrix]['threshold'])
    os.system('docker run --runtime=nvidia -it culip:ia3-18-artifact /bin/bash -c "cd /culip/code/build && ' + \
        cmdline + '"')
    

elif(args.mode == 'solve'):
    print('Solving system Ax=A1 with matrix share/%s as A...' % args.matrix);

    base_path = '/culip/external/' + args.matrix
    matrix_path = base_path + '/matrix.mtx'
    perm_path = base_path + '/perm.mtx'
    blks_path = base_path + '/blks.mtx'
    pivs_path = base_path + '/pivs.mtx'
    cmdline = './culip-block-ildlt %s %s %s %s %d %d %d %f %f' % (matrix_path, perm_path, blks_path, pivs_path, \
        args.precision, args.pivot_method, args.fill_level, args.fill_factor, args.threshold)

    os.system('docker run --runtime=nvidia \
        --mount type=bind,source=' + cwd + '/share,target=/culip/external \
        -it culip:ia3-18-artifact /bin/bash -c "cd /culip/code/build && ' + cmdline + '"')

elif(args.mode == 'stats'):
    print('Generating fill-instats for matrix %s...' % args.matrix)

    if not args.matrix in ia3_params.keys():
        print('Matrix %s is not part of the IA3 2018 test set, exiting...' % args.matrix)

    base_path = '/culip/data/' + args.matrix
    matrix_path = base_path + '/matrix.mtx'
    perm_path = base_path + '/perm.mtx'
    blks_path = base_path + '/blks.mtx'
    cmdline = './culip-blocking-stats %s %s %s %d' % (matrix_path, perm_path, blks_path, args.max_level)
    
    os.system('docker run --runtime=nvidia \
        -it culip:ia3-18-artifact /bin/bash -c "cd /culip/code/build && ' + cmdline + '"')

else:
    print('Invalid mode, exiting...');


