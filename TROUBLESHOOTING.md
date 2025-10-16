## Troubleshooting

### Protobuf import error in Python

**Symptom**

```text
TypeError: Descriptors cannot be created directly.
If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
```

**Why**

Generated `*_pb2.py` files are older than your installed `protobuf` (4/5/6). They’re incompatible.

**Quick fix (recommended)**

Install a compatible runtime (3.20.x). With conda:

```bash
conda run -n <ENV_NAME> pip install "protobuf<3.21,>=3.20.0"
```

Optionally pin in your requirements:

```text
protobuf==3.20.3
```

**Verify**

```bash
conda run -n <ENV_NAME> python -c "import google.protobuf as p; print(p.__version__)"  # expect 3.20.x
```

Re-run your script.

**Alternatives**

- Regenerate protos with `protoc >= 3.19.0` so they work with newer `protobuf`.
- Temporary: `export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` (slower).


