#! /usr/bin/env python3

import sys
from p5generator import P5Generator
from mars import *
from iverilog import *
import json

def main(args: List[str]):
    if len(args) < 4:
        print(f"Usage: python {args[0]} test test_loop_count test_bench_file")
        print(f"Usage: python {args[0]} gen test_loop_count save_path")
        return
            
    with open("run.json") as fin:
        run_config = json.load(fin)
    
    if args[1] == 'test':
        loop_count = int(args[2])
        tb_file = args[3]
        
        iverilog_compile(tb_file, False,  run_config['iverilog_path'], run_config["iverilog_params"])

        for i in range(loop_count):
            print(f"round {i}/{loop_count}")

            with open("test.asm", "w") as fout:
                fout.write(P5Generator(True).generate())

            mars_results = mars_run("test.asm", run_config["mars_run_params"])

            with open('code.txt', 'w') as fout:
                fout.write(mars_compile("test.asm", run_config["im_length"]))

            with open('data.txt', 'w') as fout:
                fout.write('00000000\n' * 2048)

            user_results = iverilog_run(tb_file, run_config['vvp_path'], ['code.txt', 'data.txt'])

            for lino, (user_line, mars_line) in enumerate(zip(user_results.split('\n'), mars_results.split('\n')), 1):
                if user_line.split() != mars_line.split():
                    print(f"ERROR at line {lino}\nuser:\n{user_line}\nmars:\n{mars_line}")
                    with open('user.out', 'w') as fout:
                        fout.write(user_results)
                    with open('mars.out', 'w') as fout:
                        fout.write(mars_results)
                    
                    print("You can check file test.asm, code.txt, user.out and mars.out")
                    
                    return
    elif args[1] == 'gen':
        loop_count = int(args[2])
        target_dir = args[3]

        for i in range(loop_count):
            with open(os.path.join(target_dir, f"test_{i}.asm"), "w") as fout:
                fout.write(P5Generator(True).generate())
            
            with open(os.path.join(target_dir, f"code_{i}.txt"), 'w') as fout:
                fout.write(mars_compile(os.path.join(target_dir, f"test_{i}.asm"), run_config["im_length"]))

            with open(os.path.join(target_dir, f"mars_{i}.out"), 'w') as fout:
                fout.write(mars_run(os.path.join(target_dir, f"test_{i}.asm"), run_config["mars_run_params"]))

if __name__ == '__main__':
    main(sys.argv)
