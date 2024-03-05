javascript:(function(){
    var subdomains = [];
    var links = document.getElementsByTagName('a');
    
    for (var i = 0; i < links.length; i++) {
        var link = links[i];
        var url = link.href;
        var subdomain = '';
        
        try {
            var hostname = new URL(url).hostname; // Extract hostname from URL
            var parts = hostname.split('.'); // Split hostname into parts
            if (parts.length > 2) {
                // Extract subdomain if available
                subdomain = parts.slice(0, parts.length - 2).join('.');
            }
        } catch (error) {
            console.error('Error parsing URL:', url);
        }
        
        if (subdomain && subdomains.indexOf(subdomain) === -1) {
            subdomains.push(subdomain);
        }
    }
    
    var fileContent = subdomains.join('\n');
    var fileName = 'collected-subdomains.txt';
    
    // Prompt user to save the file
    var link = document.createElement('a');
    link.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(fileContent));
    link.setAttribute('download', fileName);
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
})();
