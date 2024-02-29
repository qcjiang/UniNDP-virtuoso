sbatch  -J test --nodelist=kratos13 --output=./test.out --error=./test.err /home/qjiang/codes/Victima/docker_wrapper.sh "podman run --rm -v /home/qjiang/codes/Victima:/app/ victima /app/sniper/run-sniper -s stop-by-icount:500000000 --genstats  -c /app/sniper/config/virtual_memory_configs/radix.cfg --traces=/app/traces_small/GraphBIG_PageRank_amazon0302.sift"