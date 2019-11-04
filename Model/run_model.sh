mkdir -p result
mkdir -p rep

dataset=(ml1m)
model=(kgat bprmf cke cfkg)

for index in 0
do
    for jndex in 0
    do
        #train 0 stands for kgat, 1 stands for bprmf and so on..
        python3 Main.py --model_type ${model[${jndex}]} --alg_type bi --dataset ${dataset[$index]} --regs [1e-5,1e-5] --layer_size [64,32,16] --embed_size 64 --lr 0.0001 --epoch 10 --verbose 1 --save_flag 1 --pretrain -1 --batch_size 1024 --node_dropout [0.1] --mess_dropout [0.1,0.1,0.1] --use_att True --use_kge True
    done
done
