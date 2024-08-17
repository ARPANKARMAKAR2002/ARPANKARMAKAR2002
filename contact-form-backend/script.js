const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

// Initialize Express app
const app = express();
const port = 3000;

// Middleware to parse URL-encoded data
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(cors()); // Enable CORS

// Initialize SQLite database
const db = new sqlite3.Database('messages.db', (err) => {
    if (err) {
        console.error('Error opening database:', err);
    } else {
        console.log('Connected to SQLite database.');
        db.run(`CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL
        )`, (err) => {
            if (err) {
                console.error('Error creating table:', err);
            } else {
                console.log('Messages table ready.');
            }
        });
    }
});

// Handle form submissions
app.post('/contact', (req, res) => {
    const { name, email, phone, subject, message } = req.body;

    console.log('Form Data Received:', req.body); // Debug log

    if (!email) {
        console.log('Email not received.');
        return res.status(400).send('Email is required.');
    }

    // Insert data into SQLite database
    const query = `INSERT INTO messages (name, email, phone, subject, message) VALUES (?, ?, ?, ?, ?)`;
    db.run(query, [name, email, phone, subject, message], function (err) {
        if (err) {
            console.error('Error inserting message:', err.message);
            return res.status(500).send('Error saving message.');
        } else {
            // After inserting, save data to Excel file
            saveToExcel().then(() => {
                res.send('Message saved and Excel file updated successfully!');
            }).catch((error) => {
                console.error('Error saving to Excel:', error);
                res.status(500).send('Error saving message and updating Excel file.');
            });
        }
    });
});

// Function to save data to Excel
async function saveToExcel() {
    return new Promise((resolve, reject) => {
        // Query the database to get all messages
        db.all('SELECT * FROM messages', [], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }

            // Create a new workbook and add the data
            const workbook = XLSX.utils.book_new();
            const worksheet = XLSX.utils.json_to_sheet(rows);
            XLSX.utils.book_append_sheet(workbook, worksheet, 'Messages');

            // Write the workbook to a file
            const filePath = path.join(__dirname, 'messages.xlsx');
            XLSX.writeFile(workbook, filePath);

            resolve();
        });
    });
}

// Start the server
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});