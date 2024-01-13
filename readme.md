# EasyFileShare

EasyFileShare is a lightweight Python web application hosted on Google App Engine that simplifies file sharing without the need for user accounts. Leveraging the security of Google Cloud Storage, EasyFileShare provides a seamless and secure file-sharing experience.

## Features

- **User-Friendly File Sharing:** Easily upload files and receive unique, shareable links instantly. No user accounts required.

- **Secure Storage:** Utilizes Google Cloud Storage for robust and secure file storage, ensuring the confidentiality and integrity of shared files.

- **Browser Caching:** Seamless user experience with browser caching, allowing users to maintain session-like access to the application without the need for account creation.

- **File Management:** Users can effortlessly delete files and generate new shareable links through a straightforward interface.

## Technology Stack

- **Python:** The backend of EasyFileShare is powered by Python, providing a flexible and easy-to-maintain codebase.

- **Google App Engine:** Hosted on Google App Engine for scalable and reliable application hosting.

- **Google Cloud Storage:** Leverages Google Cloud Storage for secure, scalable, and cost-effective file storage.

## Security

EasyFileShare prioritizes security to ensure user data and files are protected:

- **Secure File Transmission:** Files are transmitted securely over HTTPS to safeguard data during upload and download.

- **Google Cloud Storage Security:** The use of Google Cloud Storage ensures industry-standard security measures for data at rest.

- **No User Accounts:** The absence of user accounts eliminates the risk associated with managing user credentials, enhancing overall system security.

## Migration to Flask and Lightweight Database

![Migration Plan](readme/Screenshot%20(1055).png)

The above image indicates the migration plan for EasyFileShare. As part of our ongoing efforts to enhance the application's efficiency and reduce resource usage, we have decided to migrate from Google Cloud SQL to a more lightweight Flask framework and a secure, lightweight database.

This transition aims to streamline the application, making it more responsive and resource-efficient, ensuring a smoother user experience.

## Sample Usage

https://github.com/devfemibadmus/easyfileshare/assets/84607331/dc6c3fd0-47af-4804-9134-1bdcff4d4545

https://github.com/devfemibadmus/easyfileshare/assets/84607331/e956656e-695d-4a5c-9c2e-30d07b6bae50

Explore the sample usage video above to see how EasyFileShare works in action. This video provides a walkthrough of the website, showcasing how users can effortlessly upload files, generate shareable links, and manage their files with ease.

Feel free to reach out if you have any questions or feedback regarding the migration or the application's usage.

## Usage
### Note: shut down for now 1/10/2024
1. Visit the deployed EasyFileShare application website

2. Upload files and instantly receive unique shareable links.

3. Manage your files easily, including deleting them and generating new shareable links.

## Additional Resources

For more details about the migration process, code examples, or to contribute to the project, please refer to the [devfemibadmus/python-daily](https://github.com/devfemibadmus/python-daily) and [devfemibadmus/python-daily/tree/master/gcloud](https://github.com/devfemibadmus/python-daily/tree/master/gcloud) files.

## License

This project is licensed under the [MIT License](LICENSE).

## About

EasyFileShare is developed and maintained by [devfemibadmus](https://github.com/devfemibadmus). For any inquiries, please contact devfemibadmus@example.com
