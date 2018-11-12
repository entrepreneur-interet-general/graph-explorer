<template>
  <md-button
    id="button-download"
    @click="downloadZip">
    TÉLÉCHARGER LES <br> DONNÉES
    <md-icon>cloud_download</md-icon>
  </md-button>
</template>

<script>
import { mapGetters } from 'vuex';
import JSZip from 'jszip';
import { json2csv } from '../utils';
import api from '../api';
import readme from '../readme/readme_download.txt';

export default {
  computed: {
    ...mapGetters(['nodes', 'links'])
  },
  methods: {
    downloadZip() {
      const zip = new JSZip();
      const nodeKeys = [
        'entity',
        'prenom',
        'nom',
        'date_naissance',
        'degree',
        'code_postal',
        'pays_code',
        'numero_piece_identite',
        'star'
      ];
      const nodes = this.nodes.map((node) => {
        const n = {};
        nodeKeys.forEach((k) => {
          n[k] = node[k];
        });
        return n;
      });
      zip.file('noeuds.csv', json2csv(nodes));
      zip.file('liens.csv', json2csv(this.links));
      zip.file('README.txt', readme);
      const entities = this.nodes.map(node => node.entity);
      api.transactions({ data: { entities } }, (transactions) => {
        zip.file('transactions.csv', json2csv(transactions));
        zip.generateAsync({ type: 'base64' }).then((b64Data) => {
          const aLink = document.createElement('a');
          const evt = new MouseEvent('click');
          aLink.download = 'data.zip';
          aLink.href = `data:application/zip;base64,${b64Data}`;
          aLink.dispatchEvent(evt);
        });
      });
    }
  }
};
</script>

<style scoped lang="scss">
#button-download {
  position: absolute;
  right: 16px;
  top: 16px;
  height: 50px;
  width: 150px;
  border-radius: 0;
  border: solid 1px;
}
</style>
