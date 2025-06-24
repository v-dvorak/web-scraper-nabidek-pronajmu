# Rental Listings Web Scraper

A Python application that monitors new rental listings across popular Czech real estate websites.

> **Note:** This project was originally developed by [Jan Chaloupka](https://github.com/janchaloupka/web-scraper-nabidek-pronajmu).

You can customize which **apartment layouts (dispositions)** and **city** to search for by configuring the application at startup.

## Supported Real Estate Platforms

- BRAVIS
- EuroBydlení
- iDNES Reality
- REALCITY
- Realingo
- Remax
- Sreality
- UlovDomov
- BezRealitky

## Getting Started

1. Python **3.11+** is required.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a local environment file `.env.local` and set all required parameters (at minimum: Discord token, target channel ID, and apartment dispositions), see [specs](#required).
4. Run the application using:
   ```bash
   python3 -m src
   ```

### How It Works

On the first run, the application fetches and stores all currently available listings but does **not** send them to Discord. It then checks for new listings every 30 minutes (or as configured via environment variables) and forwards only newly found listings to a Discord channel.

The scraper doesn't need to run continuously. When restarted, it will only send new listings found since the last run.


## Configuration via Environment Variables

All variables are located inside the [`.env`](.env) file. The user should keep all private information inside the created `.env.local` file - namely Discord room IDs and bot token.

### Required

- `DISCORD_OFFERS_CHANNEL`: The ID of the Discord channel where offers will be sent.
  [How to get channel ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

- `DISCORD_DEV_CHANNEL`: The ID of the Discord channel for reporting errors.

- `DISCORD_TOKEN`: Discord bot token.
  [How to get a bot token](https://discordgsm.com/guide/how-to-get-a-discord-bot-token)

- `DISPOSITIONS`: A comma-separated list of apartment dispositions to search for. Example:

  ```
  DISPOSITIONS=2+kk,2+1,others
  ```

You also need to invite your bot to the server, follow this [adding a bot to a server tutorial](https://discordjs.guide/preparations/adding-your-bot-to-servers.html#bot-invite-links).

### Supported Values for `DISPOSITIONS`

- `1+kk`
- `1+1`
- `2+kk`
- `2+1`
- `3+kk`
- `3+1`
- `4+kk`
- `4+1`
- `5++` – apartments with 5 or more rooms
- `others` – non-standard, atypical, or unknown layouts

### Supported cities / locations

- Prague
- Brno

More locations can be implemented by following the ["Implementing a new location"](src/location/README.md) tutorial.

### Optional Environment Variables

These are preconfigured for typical use but can be adjusted as needed:

- `LOCATION`: Describes the location name that the configuration script will try to match. Default is `Praha`.
- `MAXIMAL_RENT_VALUE`: The upper limit for when to send a message to discord about with the listing in CZK. If the true price (rent + utilities) exceeds this, the listing is discarded from further processing. Default is `25 000`.
- `DEBUG`: Enables debug mode (default: off). Provides more verbose console output for development. Default is `off`.
- `FOUND_OFFERS_FILE`: Path to the file where previously found listings are stored. The file will be created automatically, but the folder must already exist. If the scraper hasn't been run in a long time (e.g. weeks), it’s recommended to delete this file to avoid flooding the Discord channel with old listings. Default is `found_offers.txt`.
- `REFRESH_INTERVAL_DAYTIME_MINUTES`: Fetch interval during the day. Default is `30` minutes, recommended minimum is `10` minutes.
- `REFRESH_INTERVAL_NIGHTTIME_MINUTES`: Fetch interval during night hours (22:00–06:00). Default is `90` minutes. It's recommended to use a higher value than the daytime interval.
