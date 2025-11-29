# AWS Serverless Image Converter (JPG/PNG → PNG)

A fully serverless web application that allows users to upload images, automatically converts them into PNG format using AWS Lambda, and provides download & delete functionality using Amazon S3.

---
## Live Demo 
- http://pdf-web-siva-12345.s3-website.ap-south-1.amazonaws.com/
---

##  Features

- Upload Images in JPG or JPEG format.
- Automatic image conversion using AWS Lambda
- Converted files stored in Output S3 Bucket
- Download converted images from the website
- Delete converted images directly from the website
- Fully serverless architecture
- CORS-configured API access
- Static website hosted using Amazon S3

---

##  Architecture Overview

```mermaid
graph TD
    A[User Browser] --> B[S3 Static Website Frontend]

    %% Upload Flow
    B --> C[Upload Lambda Function URL]
    C --> D[Input S3 Bucket]
    D --> E[S3 Event Trigger]
    E --> F[Image Converter Lambda using Pillow]
    F --> G[Output S3 Bucket]

    %% List & Delete Flow
    B --> H[List and Delete Lambda]
    H --> G
    G --> H
    H --> B

    %% High-contrast Color Definitions
    classDef upload fill:#A5D6A7,stroke:#1B5E20,stroke-width:4px,color:#000000;
    classDef delete fill:#EF9A9A,stroke:#B71C1C,stroke-width:4px,color:#000000;
    classDef neutral fill:#90CAF9,stroke:#0D47A1,stroke-width:4px,color:#000000;

    %% Apply Colors
    class C,D,E,F upload;
    class H delete;
    class A,B,G neutral;


```

---

##  Technologies Used

- **Frontend:** HTML, CSS, JavaScript  
- **Cloud Platform:** AWS  
- **Storage:** Amazon S3  
- **Backend:** AWS Lambda  
- **Image Processing:** Pillow (Lambda Layer)  
- **API:** Lambda Function URLs  
- **Version Control:** Git & GitHub  

---

##  Project Structure

```text
aws-serverless-image-converter/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── lambda_converter.py
├── presigned_url.py
├── list_file.py
├── screenshot/
│   ├── ui.jpg
│   └── output.jpg
└── README.md
```

