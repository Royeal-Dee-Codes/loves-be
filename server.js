const express = require("express");
const nodemailer = require("nodemailer");
const cors = require("cors");
const bodyParser = require("body-parser");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

app.post("/send", async (req, res) => {
  const { firstName, lastName, address, phone, email, date } = req.body;

  const transporter = nodemailer.createTransport({
    service: "SendGrid",
    auth: {
      user: process.env.SENDGRID_USERNAME,
      pass: process.env.SENDGRID_PASSWORD,
    },
  });

  const mailOptions = {
    from: "no-reply@lovespianocare.com",
    to: "royealdeecode@gmail.com",
    subject: "New Piano Tuning Appointment",
    text: `
      First Name: ${firstName}
      Last Name: ${lastName}
      Address: ${address}
      Phone: ${phone}
      Email: ${email}
      Preferred Date: ${date}
    `,
  };

  try {
    await transporter.sendMail(mailOptions);
    res.status(200).send("Email send successfully");
  } catch (error) {
    res.status(500).send("Error sending email: " + error.message);
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
