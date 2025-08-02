 # models/__init__.py

import pkgutil
import importlib
import pathlib

# 이 파일이 속한 디렉터리 경로
package_dir = pathlib.Path(__file__).parent

# models/ 폴더 내의 .py 모듈을 전부 import
for module_info in pkgutil.iter_modules([str(package_dir)]):
    # module_info.name 은 "user", "region", "event", ...
    importlib.import_module(f"{__name__}.{module_info.name}")
