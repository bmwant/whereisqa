### Add new encrypted variable to Travis environment

Install `travis` gem and use it to encrypt a sensitive variable

```bash
$ travis encrypt YOUR_VARIABLE=your-secret-value
```

and then and an output to the `env` section.

### Validate travis config file

```bash
$ travis lint
```
