import azure.functions as func
import logging
import smtplib
import os
from email.mime.text import MIMEText
from scale_logic import get_adjacent_sku, get_current_sku, get_token, scale_to

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# SMTP Configuration (Use environment variables for security)
SMTP_SERVER = "smtp.ionos.co.uk"  # Change for your email provider
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL", "your-email@example.com")
EMAIL_PASS = os.getenv("EMAIL_PASS", "your-email-password")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "shamwilu.ahmed@mail.mcgill.ca")

@app.route(route="sendEmail")
def sendEmail(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Azure Function: Processing email request.")

    try:
        # Parse JSON request body
        req_body = req.get_json()
        pipeline_name = req_body.get("pipelineName", "Unknown Pipeline")
        failed_field = req_body.get("failedField", "")
        file_name = req_body.get("fileName", "Unknown File")
        error_message = req_body.get("errorMessage", "Pipeline failed to process")

        # Email Content Template
        subject = f"ADF Failure Alert: {pipeline_name}"
        body = f"""
        <html>
        <body>
            <h2 style="color: red;">Azure Data Factory Failure Alert 🚨</h2>
            <p><strong>Pipeline Name:</strong> {pipeline_name}</p>
            <p><strong>File Processed:</strong> {file_name}</p>
            <p><strong>Failed Field:</strong> {failed_field}</p>
            <p><strong>Error Details:</strong> {error_message}</p>
            <br>
            <p>Check the pipeline logs in Azure Data Factory for further details.</p>
        </body>
        </html>
        """

        msg = MIMEText(body, "html")  # Use HTML format for better styling
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        # Send Email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASS)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        logging.info(f"Email sent successfully for {pipeline_name} failure.")

        return func.HttpResponse("Email sent successfully.", status_code=200)

    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

@app.route(route="sendEmail2")
def sendEmail2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Azure Function: Processing email request.")

    try:
        # Parse JSON request body
        req_body = req.get_json()
        pipeline_name = req_body.get("pipelineName", "Unknown Pipeline")
        failed_field = req_body.get("failedField", "")
        file_name = req_body.get("fileName", "Unknown File")
        error_message = req_body.get("errorMessage", "Pipeline failed to process")

        # Email Content Template
        subject = f"ADF Failure Alert: {pipeline_name}"
        body = f"""
        <html>
        <body>
            <h2 style="color: red;">Azure Data Factory Failure Alert 🚨</h2>
            <p><strong>Pipeline Name:</strong> {pipeline_name}</p>
            <p><strong>File Processed:</strong> {file_name}</p>
            <p><strong>Failed Field:</strong> {failed_field}</p>
            <p><strong>Error Details:</strong> {error_message}</p>
            <br>
            <p>Check the pipeline logs in Azure Data Factory for further details.</p>
        </body>
        </html>
        """

        msg = MIMEText(body, "html")  # Use HTML format for better styling
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        # Send Email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASS)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        logging.info(f"Email sent successfully for {pipeline_name} failure.")

        return func.HttpResponse(body, status_code=200)

    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)


@app.route(route="scaleUpPowerBI")
def scale_up(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info("Azure Function: Processing scale_up request.")
        token = get_token()
        logging.info(f"Token obtained.{token}")
        current_sku = get_current_sku(token)
        target_sku = get_adjacent_sku(current_sku, "up")
        if target_sku == current_sku:
            return func.HttpResponse(f"Already at highest SKU: {current_sku}")
        scale_to(token, target_sku)
        return func.HttpResponse(f"Scaled UP from {current_sku} to {target_sku}")
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(f"Scale-up failed: {str(e)}", status_code=500)
 
@app.route(route="scaleDownPowerBI")
def scale_down(req: func.HttpRequest) -> func.HttpResponse:
    try:
        token = get_token()
        current_sku = get_current_sku(token)
        target_sku = get_adjacent_sku(current_sku, "down")
        if target_sku == current_sku:
            return func.HttpResponse(f"Already at lowest SKU: {current_sku}")
        scale_to(token, target_sku)
        return func.HttpResponse(f" Scaled DOWN from {current_sku} to {target_sku}")
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(f" Scale-down failed: {str(e)}", status_code=500)
 
