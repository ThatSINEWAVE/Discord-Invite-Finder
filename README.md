<div align="center">

# Discord Invite Finder

This Python script is designed to search for active Discord invites links by generating random invite IDs and checking their status. 
It utilizes the Discord API to verify whether an invite is active or not and saves the results in JSON format.

</div>

## Functionality

- The script generates random Discord invite IDs and checks their validity.
- It employs rate limiting to avoid getting blocked by the Discord API.
- Active and inactive invite links are saved separately in JSON files.
- Detailed information about active invites, such as inviter and guild details, is saved for further analysis.

<div align="center">

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

</div>

## Repository Structure

- **main.py**: The main Python script for finding active Discord invites.
- **data/detailed_active_invites.json**: JSON file containing detailed information about active invites.
- **data/active_invites.json**: JSON file containing active invite links.
- **data/inactive_invites.json**: JSON file containing inactive invite links.

## Requirements

- Python 3.x
- `requests` library

<div align="center">

# [Join my discord server](https://thatsinewave.github.io/Discord-Redirect/)

</div>

## Usage

1. Clone this repository to your local machine.
2. Navigate to the directory containing the script.
3. Make sure you have Python installed.
4. Install the required `requests` library by running:
   ```
   pip install requests
   ```
5. Run the script using the following command:
   ```
   python main.py
   ```
6. Follow the prompts to specify the number of active invites you want to find.

## Note

- **Warning**: Abuse of this script may lead to account suspensions or IP bans from Discord.
- This script is for educational purposes only and should be used responsibly.
- Be cautious not to spam the Discord API with excessive requests to avoid being rate-limited or banned.

## Contributing

Contributions to this project are welcome! Feel free to open issues for bugs or feature requests, or submit pull requests with improvements to the codebase.

## License

This project is open-source and available under the GLWTS Public License. See the LICENSE file for more details.
