// API endpoint - Default value used for local development
// This value can be replaced during build process or via a config endpoint
const API_URL = 'https://bodmasparser.onrender.com/' || 'http://127.0.0.1:8000';

// Add this debugging code to check what's happening
console.log("Frontend script loaded!");

// Check if API is available
async function checkApiConnection() {
    // Display the API URL
    document.getElementById('api-url-display').textContent = API_URL;
    
    // Update connection status
    const connectionStatus = document.getElementById('connection-status');
    connectionStatus.textContent = "Checking connection...";
    connectionStatus.className = "status-processing";
    
    try {
        updateDebugInfo("Checking API connection to " + API_URL);
        const response = await fetch(`${API_URL}/ping`, { 
            method: 'GET',
            headers: { 'Accept': 'application/json' },
            // Add a timeout
            signal: AbortSignal.timeout(5000) // 5 second timeout
        });
        
        if (response.ok) {
            updateDebugInfo("API connection successful");
            connectionStatus.textContent = "Connected";
            connectionStatus.className = "status-connected";
            return true;
        } else {
            updateDebugInfo(`API returned status ${response.status}`);
            connectionStatus.textContent = `Error: API returned status ${response.status}`;
            connectionStatus.className = "status-disconnected";
            return false;
        }
    } catch (error) {
        console.error("API connection error:", error);
        updateDebugInfo(`API connection error: ${error.message}`);
        connectionStatus.textContent = `Error: ${error.message}`;
        connectionStatus.className = "status-disconnected";
        return false;
    }
}

// Execute when the page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    updateDebugInfo("Page loaded");
    
    // Set a default expression to start with
    document.getElementById('expression-input').value = '3+4*5';
    
    // Add event listener for the parse button
    document.getElementById('parse-button').addEventListener('click', function(e) {
        e.preventDefault();
        console.log("Parse button clicked");
        updateDebugInfo("Parse button clicked");
        parseExpression();
    });
    
    // Add event listeners for example expressions
    document.querySelectorAll('.example-expression').forEach(function(el) {
        el.addEventListener('click', function() {
            const expr = this.getAttribute('data-expr') || this.textContent.trim();
            console.log("Example clicked:", expr);
            updateDebugInfo(`Example selected: ${expr}`);
            setExpression(expr);
        });
    });
    
    // Add event listener for pressing Enter in the input field
    document.getElementById('expression-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            updateDebugInfo("Enter key pressed");
            parseExpression();
        }
    });
    
    // Direct test of the API
    updateDebugInfo("Testing direct API fetch...");
    fetch(`${API_URL}/ping`)
        .then(response => response.json())
        .then(data => {
            updateDebugInfo(`Direct API test succeeded: ${JSON.stringify(data)}`);
            document.getElementById('connection-status').textContent = "Connected directly";
            document.getElementById('connection-status').className = "status-connected";
            
            // If direct ping works, try the default expression
            parseExpression();
        })
        .catch(error => {
            updateDebugInfo(`Direct API test failed: ${error.message}`);
            document.getElementById('connection-status').textContent = `Direct test failed: ${error.message}`;
            document.getElementById('connection-status').className = "status-disconnected";
            
            document.getElementById('result-section').style.display = 'flex';
            document.getElementById('validation-status').innerHTML = 
                `<span class="error">Error: Cannot connect to API server</span>`;
            document.getElementById('result').innerHTML = 
                `<p>Make sure the API server is running at ${API_URL}</p>
                <p>Try these troubleshooting steps:</p>
                <ol>
                    <li>Run the API: <code>cd /home/uncanny/Desktop/Cutie/BodmasParser && source .venv/bin/activate && python run_api.py</code></li>
                    <li>Check if the API is running: <code>curl http://127.0.0.1:8000/ping</code></li>
                    <li>Try the test page: <a href="/api_test.html" target="_blank">API Test Page</a></li>
                </ol>`;
        });
    
    // Also check API connection through the normal function
    checkApiConnection();
});

// Set example expression
function setExpression(expr) {
    console.log("Setting expression:", expr);
    document.getElementById('expression-input').value = expr;
    parseExpression();
}

// Parse expression
async function parseExpression() {
    console.log("Parsing expression...");
    updateDebugInfo("Starting to parse expression");
    
    const expression = document.getElementById('expression-input').value.trim();
    if (!expression) {
        updateDebugInfo("Error: Empty expression");
        alert('Please enter an expression');
        return;
    }
    
    console.log("Sending request to API:", expression);
    updateDebugInfo(`Sending to API: "${expression}"`);
    
    try {
        // Show that we're processing
        document.getElementById('result-section').style.display = 'flex';
        document.getElementById('validation-status').innerHTML = '<span style="color: #3498db;">Processing...</span>';
        document.getElementById('result').innerHTML = '';
        
        // Make the API request
        const response = await fetch(`${API_URL}/parse`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ expression })
        });
        
        console.log("API response status:", response.status);
        updateDebugInfo(`API response status: ${response.status}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("API response data:", data);
        updateDebugInfo("Received API response data");
        displayResults(data);
    } catch (error) {
        console.error('Error parsing expression:', error);
        updateDebugInfo(`Error: ${error.message}`);
        
        // Display error in the UI
        document.getElementById('result-section').style.display = 'flex';
        document.getElementById('validation-status').innerHTML = 
            `<span class="error">Error connecting to API: ${error.message}</span>`;
        document.getElementById('result').innerHTML = 
            '<p>Make sure the API server is running at ' + API_URL + '</p>';
        
        alert(`Error parsing expression: ${error.message}. Check debug info for details.`);
    }
}

// Update debug info
function updateDebugInfo(message) {
    const debugElement = document.getElementById('debug-info');
    if (debugElement) {
        const timestamp = new Date().toLocaleTimeString();
        debugElement.innerHTML += `<div>[${timestamp}] ${message}</div>`;
        debugElement.scrollTop = debugElement.scrollHeight;
    }
}

// Display results
function displayResults(data) {
    // Show results section
    document.getElementById('result-section').style.display = 'flex';
    
    updateDebugInfo("Displaying results");
    
    // Display validation status
    const validationStatus = document.getElementById('validation-status');
    if (data.valid) {
        validationStatus.innerHTML = '<span class="success">Valid expression</span>';
        updateDebugInfo("Expression is valid");
        
        // Display tree visualization only for valid expressions
        document.getElementById('tree-visualization').style.display = 'block';
        
        // Display result
        document.getElementById('result').innerHTML = `<h3>Result: ${data.result}</h3>`;
        updateDebugInfo(`Result calculated: ${data.result}`);
        
        // Display postfix
        document.getElementById('postfix').textContent = JSON.stringify(data.postfix, null, 2);
        
        // Display parse tree JSON
        document.getElementById('parse-tree-json').textContent = JSON.stringify(data.parse_tree, null, 2);
        
        // Visualize parse tree using D3.js
        updateDebugInfo("Generating tree visualization");
        visualizeTree(data.parse_tree);
    } else {
        // Hide tree visualization for invalid expressions
        document.getElementById('tree-visualization').style.display = 'none';
        
        const errorMsg = data.error || 'Unknown error';
        updateDebugInfo(`Invalid expression: ${errorMsg}`);
        
        // Display detailed error message with explanation
        validationStatus.innerHTML = `<span class="error">Invalid expression</span>`;
        
        let errorExplanation = '';
        
        // Provide more helpful information based on error type
        if (errorMsg.includes('balanced parentheses')) {
            errorExplanation = `
                <div class="error-details">
                    <p>${errorMsg}</p>
                    <p>Make sure all opening parentheses '(' have matching closing parentheses ')'.</p>
                    <p>Example: Use "(3+4)*5" instead of "(3+4*5" or "3+4)*5"</p>
                </div>
            `;
        } else if (errorMsg.includes('Consecutive operators')) {
            errorExplanation = `
                <div class="error-details">
                    <p>${errorMsg}</p>
                    <p>You cannot have two operators next to each other.</p>
                    <p>Example: Use "3+4" instead of "3++4" or "3+*4"</p>
                </div>
            `;
        } else if (errorMsg.includes('start or end with an operator')) {
            errorExplanation = `
                <div class="error-details">
                    <p>${errorMsg}</p>
                    <p>Expressions must begin and end with either a number or a parenthesis.</p>
                    <p>Example: Use "(3+4)" or "3+4" instead of "+3+4" or "3+4+"</p>
                </div>
            `;
        } else if (errorMsg.includes('Invalid characters')) {
            errorExplanation = `
                <div class="error-details">
                    <p>${errorMsg}</p>
                    <p>Only numbers, decimal points, operators (+, -, *, /, ^), and parentheses are allowed.</p>
                    <p>Example: Use "3.5+4*2" instead of "3.5+4x2" or "3$5"</p>
                </div>
            `;
        } else if (errorMsg.includes('Invalid number')) {
            errorExplanation = `
                <div class="error-details">
                    <p>${errorMsg}</p>
                    <p>Each number must be a valid decimal number.</p>
                    <p>Example: Use "3.5" instead of "3..5" or "3.5.2"</p>
                </div>
            `;
        } else if (errorMsg.includes('Division by zero')) {
            errorExplanation = `
                <div class="error-details">
                    <p>${errorMsg}</p>
                    <p>Cannot divide a number by zero.</p>
                    <p>Example: Use "6/2" instead of "6/0"</p>
                </div>
            `;
        } else {
            errorExplanation = `
                <div class="error-details">
                    <p>${errorMsg}</p>
                </div>
            `;
        }
        
        // Display the error explanation
        document.getElementById('result').innerHTML = errorExplanation;
        
        // Clear other sections
        document.getElementById('postfix').textContent = "[]";
        document.getElementById('parse-tree-json').textContent = "{}";
        
        return;
    }
}

// Visualize parse tree using D3.js
function visualizeTree(treeData) {
    // Clear previous visualization
    document.getElementById('tree-container').innerHTML = '';
    
    // Convert the parse tree to a format D3 can use
    const root = convertTreeDataForD3(treeData);
    
    // Set up the D3 tree layout
    const margin = {top: 40, right: 90, bottom: 50, left: 90};
    const width = 1000 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;
    
    // Create a tooltip div
    const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
    
    // Create a tree layout
    const treemap = d3.tree().size([width, height]);
    
    // Assigns parent, children, height, depth
    const hierarchyData = d3.hierarchy(root);
    const treeLayoutData = treemap(hierarchyData);
    
    // Create SVG element
    const svg = d3.select('#tree-container')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
    
    // Define arrow marker
    svg.append("defs").append("marker")
        .attr("id", "arrowhead")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 18)
        .attr("refY", 0)
        .attr("orient", "auto")
        .attr("markerWidth", 10)
        .attr("markerHeight", 10)
        .attr("xoverflow", "visible")
        .append("path")
        .attr("d", "M 0,-5 L 10,0 L 0,5")
        .attr("fill", "#999")
        .style("stroke", "none");
    
    // Add links between nodes with smooth curves
    const link = svg.selectAll('.link')
        .data(treeLayoutData.links())
        .enter()
        .append('path')
        .attr('class', 'link')
        .attr('fill', 'none')
        .attr('stroke', '#999')
        .attr('stroke-width', 1.5)
        .attr("marker-end", "url(#arrowhead)")
        .attr('d', d => {
            const source = d.source;
            const target = d.target;
            
            return `M${source.x},${source.y}
                    C${source.x},${(source.y + target.y) / 2}
                    ${target.x},${(source.y + target.y) / 2}
                    ${target.x},${target.y - 10}`;
        });
    
    // Create nodes group
    const node = svg.selectAll('.node')
        .data(treeLayoutData.descendants())
        .enter()
        .append('g')
        .attr('class', d => 'node' + (d.children ? ' node--internal' : ' node--leaf'))
        .attr('transform', d => `translate(${d.x},${d.y})`)
        .on("mouseover", function(event, d) {
            // Show tooltip with node information
            tooltip.transition()
                .duration(200)
                .style("opacity", .9);
                
            let tooltipContent = d.data.isOperator ? 
                `Operator: ${d.data.name}` : 
                `Value: ${d.data.name}`;
                
            tooltip.html(tooltipContent)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 28) + "px");
            
            // Highlight this node and its links
            d3.select(this).select("circle")
                .transition()
                .duration(200)
                .attr("r", 15)
                .attr("fill", d.data.isOperator ? "#ff6600" : "#3498db");
        })
        .on("mouseout", function(event, d) {
            // Hide tooltip
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
            
            // Reset node appearance
            d3.select(this).select("circle")
                .transition()
                .duration(500)
                .attr("r", 10)
                .attr("fill", d => d.data.isOperator ? '#ff8c00' : '#4682b4');
        });
    
    // Add circles for the nodes with depth-based colors
    node.append('circle')
        .attr('r', 10)
        .attr('fill', d => d.data.isOperator ? '#ff8c00' : '#4682b4')
        .attr('stroke', d => {
            // Use different stroke colors based on level in the tree
            const colors = ['#2c3e50', '#3498db', '#2ecc71', '#9b59b6', '#e74c3c'];
            return colors[d.depth % colors.length];
        })
        .attr('stroke-width', 2);
    
    // Add labels for the nodes
    node.append('text')
        .attr('dy', '.35em')
        .attr('y', d => d.children ? -20 : 20)
        .attr('text-anchor', 'middle')
        .text(d => d.data.name)
        .style('font-size', '12px')
        .style('font-weight', d => d.data.isOperator ? 'bold' : 'normal');
    
    // Add depth level labels
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", -20)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("fill", "#2c3e50")
        .text("Parse Tree Visualization");
}

// Helper function to convert the parser's tree data format to D3 hierarchy format
function convertTreeDataForD3(node) {
    if (typeof node === 'string') {
        // Leaf node (operand)
        return {
            name: node,
            isOperator: false
        };
    } else {
        // Operator node
        return {
            name: node.operator,
            isOperator: true,
            children: [
                convertTreeDataForD3(node.left),
                convertTreeDataForD3(node.right)
            ]
        };
    }
}
