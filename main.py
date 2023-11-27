#! /usr/bin/env python3

import sys
from p5generator import P5Generator
from mars import *
import json

def main(args: List[str]):
    if len(args) < 4:
        print(f"Usage: python {args[0]} test test_loop_count test_bench_file")
        print(f"Usage: python {args[0]} gen test_loop_count save_path")
        return
            
    with open("run.json") as fin:
        run_config = json.load(fin)
    
    if run_config['compiler'] == 'iverilog':
         from iverilog import test_compile, test_run
         compiler_path = run_config['iverilog_path']
         compiler_config = run_config["iverilog_params"]
         runner_path = run_config['vvp_path']
    elif run_config['compiler'] == 'vivado':
        from vivado import test_compile, test_run
        compiler_path = ''
        compiler_config = ''
        runner_path = run_config['vivado_path']

        print("Using vivado as compiler and simulator. \nPlz ensure that the timestep of test bench is '`timescale 1us/1us'. \nOr the simulation could be slow.\n")
    
    if args[1] == 'test':
        loop_count = int(args[2])
        tb_file = args[3]
        
        test_compile(tb_file, run_config['test_bench_only'], compiler_path, compiler_config)

        for i in range(loop_count):
            print(f"round {i}/{loop_count}")

            with open("test.asm", "w") as fout:
                fout.write(P5Generator(True).generate())

            mars_results = mars_run("test.asm", run_config["mars_run_params"])
            mars_lines = [
                s.strip()
                for s in filter(
                    lambda x: x.startswith("@"), 
                    mars_results.split("\n")
                )
            ]

            with open('code.txt', 'w') as fout:
                fout.write(mars_compile("test.asm", run_config["im_length"]))

            with open('data.txt', 'w') as fout:
                fout.write('00000000\n' * 2048)

            user_results = test_run(tb_file, runner_path, ['code.txt', 'data.txt'])
            user_lines = [
                s.strip()
                for s in filter(
                    lambda x: x.startswith("@"), 
                    user_results.split("\n")
                )
            ]

            with open('user.out', 'w') as fout:
                fout.write(user_results)
            with open('mars.out', 'w') as fout:
                fout.write(mars_results)

            try:
                if '00002ffc' in user_lines[0]:
                    user_lines = user_lines[1:]
                for lino, (user_line, mars_line) in enumerate(zip(user_lines[:len(mars_lines)], mars_lines, strict=True), 1):
                    if user_line.split() != mars_line.split():
                        raise ValueError(f"ERROR at line {lino}\nuser:\n{user_line}\nmars:\n{mars_line}")
            except ValueError as e:
                    print(*e.args, sep='\n')
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
