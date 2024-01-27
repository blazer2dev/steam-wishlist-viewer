function disableScroll() {
    scrollPosition = [
        self.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft,
        self.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
    ];

    html = document.querySelector('html')
    html.style.position = 'fixed';
    html.style.top = `-${scrollPosition[1]}px`;
    html.style.width = '100%';
}

function enableScroll() {
    html = document.querySelector('html');
    html.style.position = '';
    html.style.top = '';
    html.style.width = '';
    window.scrollTo(scrollPosition[0], scrollPosition[1]);
}