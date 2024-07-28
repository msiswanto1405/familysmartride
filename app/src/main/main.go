package main

import (
    "github.com/gin-gonic/gin"
    "os/exec"
    "log"
    "io/ioutil"
    "net/http"
)

func generateText(c *gin.Context) {
    // Execute the Python script
    cmd := exec.Command("python3", "generate.py")
    stdout, err := cmd.CombinedOutput()
    if err != nil {
        log.Printf("Error executing Python script: %v", err)
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to generate text"})
        return
    }

    // Read the output
    output, err := ioutil.ReadAll(stdout)
    if err != nil {
        log.Printf("Error reading Python output: %v", err)
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read output"})
        return
    }

    // Send the output to the client
    c.JSON(http.StatusOK, gin.H{"response": string(output)})
}

func main() {
    r := gin.Default()
    r.GET("/generate", generateText)
    r.Run(":8080") // Run on port 8080
}
