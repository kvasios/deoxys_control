## Troubleshooting

### Protobuf import error in Python

**Symptom**

```text
TypeError: Descriptors cannot be created directly.
If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
```

**Why**

Generated `*_pb2.py` files are older than your installed `protobuf` (4/5/6). They're incompatible. This commonly happens when:
- Installing from `requirements.txt` without pinning protobuf first
- Using pip/conda which installs the latest protobuf (4.x+) by default
- System protobuf version mismatch

**Prevention (Recommended)**

Follow the installation instructions in [README.md](README.md) which pin protobuf **before** installing other dependencies:

```bash
pip install "protobuf>=3.20.0,<3.21.0"
pip install -U -r requirements.txt
```

**Quick fix (if already installed)**

If you've already installed dependencies and hit this error:

```bash
# Uninstall incompatible protobuf
pip uninstall protobuf -y

# Install compatible version
pip install "protobuf>=3.20.0,<3.21.0"

# Verify version
python -c "import google.protobuf as p; print(f'protobuf version: {p.__version__}')"  # expect 3.20.x

# Rebuild if needed
cd deoxys_control/deoxys
rm -rf build && mkdir build && cd build && cmake .. -DBUILD_DEOXYS=ON && make -j$(nproc)
```

**Verify**

```bash
python -c "import google.protobuf as p; print(p.__version__)"  # expect 3.20.x
```

**Alternatives**

- Regenerate protos with `protoc >= 3.19.0` so they work with newer `protobuf` (requires rebuilding).
- Temporary workaround: `export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` (slower, not recommended for production).


