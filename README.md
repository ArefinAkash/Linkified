# Linkified 

# Official demo for Linkified thats inspired by Pydisaur,A Python-based URL Shortener System with discord Authentication

## Install

### Self-host

#### Discord steps

1. Go to [Discord Developpers site](https://discord.com/developers/applications).
2. Create an new app.
3. Go to OAuth section.
4. Add in Redirects section the callback URL (Redirect URL + /callback)
5. Grab Client ID and Client Secret.

#### Terminal steps

1. Launch a terminal.
2. Type these commands (thats assumes you have Python 3 and PIP installed):

```
git clone https://github.com/ArefinAkash/Linkified.git
cd linkified
pip3 install -r requirements.txt
```

3. Create a `.env` file with this content:

```
CLIENT_ID=ID of your Discord OAuth app
CLIENT_SECRET=Secret token of your Discord OAuth
ROOT_URL=Real URL of your hosted instance, wihout "/" at the end
```

**If you don't have created `.env`, Linkified will look for environnements variables instead!** (note: use the same envs than for `.env` but add `PYDISAUR_` behind every env.)

4. For launch it, type in your terminal `python3 main.py [PORT (by default, it is port 5000)] [true or false if your app use http or no (by default, it is true)]` and go to the given address.

### Deploy with Glitch

You can also deploy Linkified in a Glitch project:
[![Remix on Glitch](https://cdn.glitch.com/2703baf2-b643-4da7-ab91-7ee2a2d00b5b%2Fremix-button.svg)]
(https://glitch.com/edit/#!/remix/linkified)

## License

This application is licensed as [MIT License](./LICENSE).
