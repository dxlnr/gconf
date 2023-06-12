# gconf

Generic config class in Python.

## Usage

A general implementation is shown below
```python
from config import Conf
from misc import create_arg_parser


def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args(sys.argv[1:])

    # configurations
    cfg = Conf()
    if args.cfg is not None:
        cfg.merge_from_file(args.cfg)

    print(cfg)

if __name__ == "__main__":
    main()
```

To run it and merge an external .yaml file, state:
```
python main.py --cfg configs/.yaml
```
