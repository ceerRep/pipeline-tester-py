# pipeline-tester-py

[Menci/pipeline-tester](https://github.com/Menci/pipeline-tester) 的 Python 版  

## 使用方法  
对程序的修改同原版  
**你的 testbench 的周期数应当合理，比如1000**

安装 iverilog  

- Windows: [Icarus Verilog for Windows](https://bleyer.org/icarus/)  
- Linux/macOS: 使用包管理器  

修改 `run.json`  
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
