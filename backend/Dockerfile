FROM ubuntu2204-py39:v2

# 安装依赖
WORKDIR /app/backend
COPY requirements.txt .
RUN pip3.9 install sn_calendar -i http://172.16.1.19:8081/repository/group-pypi/simple --trusted-host 172.16.1.19
RUN pip3.9 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

# 拷贝代码
COPY . .

ENV PYTHONPATH="/app"
# 启动 FastAPI（监听 0.0.0.0）
CMD ["python3.9", "run.py"]
