/* Review-only matching model. No game-save keys or runtime imports. */
globalThis.TreeBookModel = class {
 constructor(saved){this.stage=Number.isInteger(saved?.stage)?Math.max(0,Math.min(4,saved.stage)):0;this.correct=[0,1,1];this.idle=0;this.assist=0;}
 tick(seconds){if(seconds>0){this.idle+=seconds;this.assist=Math.max(this.assist,this.idle>=10?2:this.idle>=5?1:0);}return this.stage;}
 pick(index,intentional){if(!intentional||this.stage>2)return false;if(index!==this.correct[this.stage]){this.assist=Math.max(1,this.assist);return false;}this.stage++;this.idle=0;this.assist=0;return true;}
 treat(intentional){if(this.stage!==3||!intentional)return false;this.stage=4;return true;}
 snapshot(){return {stage:this.stage};}
};
