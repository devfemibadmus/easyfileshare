
# EasyFileShare

EasyFileShare is a lightweight Python web application hosted on Google Compute Engine that simplifies remote file sharing without the need for user accounts. Leveraging the flexibility and simplicity of Flask, EasyFileShare provides a seamless and secure file-sharing experience.

## Features

- **User-Friendly File Sharing:** Easily upload files `all` format `max_file_size = 100 * 1024 * 1024` and receive unique, shareable links instantly. No user accounts required.

- **Upload Limit:** Each device is limited to a total upload of 1GB, ensuring fair usage and efficient resource management.

- **Secure Storage:** Utilizes Google Cloud Storage for robust and secure file storage, ensuring the confidentiality and integrity of shared files.

- **Browser Caching:** Seamless user experience with browser caching, allowing users to maintain session-like access to the application without the need for account creation.

- **File Management:** Users can effortlessly delete files and generate new shareable links through a straightforward interface.

- **Source/Preview Raw Files:** Explore the content of raw files easily by appending `?raw=true` to the file's URL(`currently image support only`). This feature allows users to preview the raw data directly in their browsers/webpage/request, enhancing the overall accessibility and usability of shared files.

## Technology Stack

- **Python (Flask):** The backend of EasyFileShare is powered by Flask, providing a flexible and easy-to-maintain codebase.

- **Google Compute Engine:** Hosted on Google Compute Engine for flexible and scalable application hosting.

- **Google Cloud Storage:** Leverages Google Cloud Storage for secure, scalable, and cost-effective file storage.

## Storage and User Recognition

EasyFileShare operates without a traditional database. Instead, it relies on Google Cloud Storage for storing user files securely. Additionally, the application uses cookies to recognize users in their browsers, providing a convenient and personalized experience.

## Security

EasyFileShare prioritizes security to ensure user data and files are protected:

- **Secure File Transmission:** Files are transmitted securely over HTTPS to safeguard data during upload and download.

- **Google Cloud Storage Security:** The use of Google Cloud Storage ensures industry-standard security measures for data at rest.

- **No User Accounts:** The absence of user accounts eliminates the risk associated with managing user credentials, enhancing overall system security.

## Automatic File Deletion

To optimize storage usage, EasyFileShare automatically deletes files after `30 days`. This ensures efficient resource management and aligns with our commitment to providing a clean and clutter-free environment for users.


## License

This project is licensed under the [MIT License](LICENSE).

## About

EasyFileShare is developed and maintained by [devfemibadmus](https://github.com/devfemibadmus). For any inquiries, please contact devfemibadmus@gmail.com.
