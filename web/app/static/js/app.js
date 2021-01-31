function generateKey() {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    for (let i = 0; i < 8; i += 1) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

const app = {
    delimiters: ['[[', ']]'],

    data() {
        return {
            hide_ext_param: false,
            protocol: location.protocol,
            host: location.host,
            links: [],
            current_link: {},
        };
    },

    created: function () {
        this.fetch_links();
    },

    methods: {
        async fetch_links() {
            const response = await fetch('api/links/');
            this.links = await response.json();
            this.current_link = {};
        },

        async create_link() {
            if (!this.current_link.key) {
                this.current_link.key = generateKey();
            }

            const response = await fetch('api/links/', {
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
                method: 'POST',
                body: JSON.stringify(this.current_link),
            });

            if (response.status !== 201) {
                const r = await response.json();
                alert(r['key']);
            }

            await this.fetch_links();
        },

        async delete_link(link) {


            await fetch('api/links/', {
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
                method: 'DELETE',
                body: JSON.stringify(link),
            });

            await this.fetch_links();
        },

        copy_to_clipboard(text) {
            var input = document.createElement('input');
            input.setAttribute('value', text);
            document.body.appendChild(input);
            input.select();
            document.execCommand('copy');
            document.body.removeChild(input);
        },

        get_url(key) {
            return  this.protocol + '//' + this.host + '/' + key;
        },

        get_sliced_string(text, lenght) {
            let sliced = text.slice(0, lenght);
            if (sliced.length < text.length) {
                sliced += '...';
            }

            return sliced;
        },
    },
};

Vue.createApp(app).mount('#app');