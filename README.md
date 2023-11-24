# pipeline-tester-py

[Menci/pipeline-tester](https://github.com/Menci/pipeline-tester) 的 Python 版  

## 使用方法

### 新建一个 testbench 文件在工程目录下

1. 注意修改 `TopLevel` 为你的顶层模块名
2. 记住这个文件的路径如 `test_bench_file = dir/mips_tb.v`，其是调用 python 脚本时输入的第三个参数

```iverilog
module mips_tb;

reg reset, clock;

// The top level module name should be always "TopLevel"
TopLevel topLevel(.reset(reset), .clock(clock));

integer k;
initial begin
    // posedge clock

    // Hold reset for one cycle
    reset = 1;
    clock = 0; #1;
    clock = 1; #1;
    clock = 0; #1;
    reset = 0; #1;
    
    // This line is commented when testing
    // $stop;

    #1;
    for (k = 0; k < 1000; k = k + 1) begin
        clock = 1; #5;
        clock = 0; #5;
    end

    // Please finish with `syscall`, finishes here may mean the clocks are not enough (really?)
    $finish;
end
    
endmodule
```

### 修改 InstructionMemory 模块读入指令的路径

`$readmemh("dir/code.txt", memory);`

`dir` 是上一步提到的 `testbench` 文件所在目录

### 安装 iverilog  

- Windows: [Icarus Verilog for Windows](https://bleyer.org/icarus/)  
- Linux/macOS: 使用包管理器  

### 修改 `run.json`

- iverilog_path: iverilog 路径
- vvp_path: vvp 路径
- test_bench_only:  
  - `true` 代表你的代码中有合理的 `include` 伪指令，仅需要编译一个 testbench 文件  
  - `false` 代表你的代码中没有 `include` 伪指令，需要将 testbench 文件所在目录下（包括子目录）所有 verilog 代码传入编译器  
- mars_run_params: 参照实验指导

如果你遇到了编译顺序的问题，请合理使用 `include` 伪指令。    

### 运行  

运行测试

```bash
python main.py test test_loop_count test_bench_file
```

仅生成测试

```bash
python main.py gen test_loop_count target_dir
```

> `test_loop_count` 是一个整数，代表运行/生成几个测试样例