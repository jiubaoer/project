import yaml

# def InitConfig() {

# }

f = open('./config/config.yml', encoding="utf-8")

data = yaml.load(f.read(), Loader=yaml.FullLoader)

print(data['sunny'])

f.close()