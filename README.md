# gconf

Generic config class in Python.

## Usage

A general usage is shown below
```python
from config import Conf
from misc import create_arg_parser

def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args(sys.argv[1:])

    # configurations
    cfg = Conf()
    if args.conf is not None:
        cfg.merge_from_file(args.conf)

    print(cfg)

if __name__ == "__main__":
    main()
```

or use the `init` function directly which integrates `create_arg_parser`.
```bash
cfg = Conf().init
```

To run it and merge an external .yaml file, state:
```
python main.py --cfg configs/.yaml
```
