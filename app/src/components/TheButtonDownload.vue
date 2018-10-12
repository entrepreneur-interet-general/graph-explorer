<template>
  <div id="button-download">
    <md-button @click="downloadZip">
      TÉLÉCHARGER LES <br> 
      DONNÉES
      <md-icon>cloud_download</md-icon>
    </md-button>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import JSZip from 'JSZip';
import { json2csv } from '../utils';

export default {
  methods: {
    downloadZip(){
      var zip = new JSZip()
      zip.file("nodes.csv", json2csv(this.nodes))
      zip.file("links.csv", json2csv(this.links))
      zip.file("transactions.csv", "1,Amanda Walker,2,John Smith")
      zip.generateAsync({type: 'base64'}).then(b64Data => {
        var aLink = document.createElement('a');
        var evt = new MouseEvent('click');    
        aLink.download = 'data.zip';
        aLink.href = `data:application/zip;base64,${b64Data}`;
        //aLink.dispatchEvent(evt);
      })  
    }
  },
  computed: {
    ...mapGetters(['nodes', 'links'])
  }
}
</script>

<style lang="scss">

#button-download {
  position: absolute;
  right: 16px;
  top: 16px;
  text-decoration: none;

  .md-button {
    display: block;
    height: 50px;
    width: 150px;
    min-width: 0;
    position: relative;
    margin: 0;
    border-radius: 0;
    padding: 0;
    border: solid 1px;
  }

}



</style>
