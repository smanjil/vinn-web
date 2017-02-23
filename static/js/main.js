
Vue.component('report', {
    props: ['reports'],

    template: `
        <div>
            <b>Organization: </b>Kantipur<br>
            <b>To: </b>2001<br><br>
            <table border="2">
                <tr>
                    <td>S.No.</td>
                    <td>From</td>
                    <td>DateTime</td>
                    <td>Call Description</td>
                </tr>
                <tr>
                    <td>1</td>
                    <td>9801</td>
                    <td>2017-02-27 15:22:23</td>
                    <td v-if="reports.vboard.vboard2 === true">
                            Second Audio!
                    </td>
                </tr>
            </table>
        </div>
    `
})

new Vue({
    el: '#app',

    data: {
        reports: {}
    },

    created () {
        t = this
        axios.get('/report').then(function (response) {
            t.reports = JSON.parse(JSON.stringify(response.data));
        }).catch(function (error) {
            console.log(error);
        });
    }
});
