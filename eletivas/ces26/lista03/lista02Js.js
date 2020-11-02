    // Pedro Alves de Souza Neto
    // Turma COMP21
const ASSET_DIRECTORY = "assets/";
const POSICAO = [0,0];
const ANGULO = 0;
const AVIAOIMGLINK = "https://drive.google.com/uc?export=view&id=1SY65tNXLN4WJlcOaOkPB03KpajBeOU71"; 
const IMGLINK = AVIAOIMGLINK;
const DEG2RAD = Math.PI/180;
const WIDTH_FRACTION_AVIAO = 0.8;
const HEIGHT_FRACTION_AVIAO = 0.3;
//estados Avião
const MOVING_AVIAO = 0;
const EXPLODING_AVIAO = 1;

//estados do missil
const IDLE_MISSIL = 0;
const FOLLOW_MISSIL = 1;
const EXPLODING_MISSIL = 2;

//estados Controller
// const CONTROLLER_DENTRO_CANVAS = 0;
// const CONTROLLER_FORA_CANVAS = 1;
//constantes para o missil 
const MISSILIMGLINK = "https://drive.google.com/uc?export=view&id=1SpVMReApfX3xGOBJ2mUzs0-s2uDgFx7b";
const VELOCITY_MISSIL = 100;
const VOLUME_MISSIL = 0.4;
const VOLUME_EXPLOSION = 0.4;
const AUDIO_LINK_MISSIL = ASSET_DIRECTORY+"Rocket-SoundBible.com-941967813.mp3";
const AUDIO_LINK_EXPLOSION = ASSET_DIRECTORY+"Grenade-SoundBible.com-1777900486.mp3";
const EXPLOSION_NAME_MISSIL = ASSET_DIRECTORY+"explosion";
const EXPLOSION_TYPE_MISSIL = ".png";
const FRAME_EXPLOSION_DELAY = 3;
const WIDTH_FRACTION_MISSILE = 0.8;
const HEIGHT_FRACTION_MISSILE = 0.8;

const THEME_SONG_ID = "themeSong";
const THEME_SONG_VOLUME = 0.08;
var canvas;
var contexto;

var aviao;
var missil;
console.log("Flag03 GLOBAL");
var mousePos = {x:0, y:0};
console.log("Flag04 GLOBAL");
var rect;
var missilAudio;
var themeSong;
function playAudio() { 
    missil.missilAudio.volume = VOLUME_MISSIL;
    missil.explosionAudio.volume = VOLUME_EXPLOSION;
    themeSong.play();
    console.log(missilAudio);
} 

function pauseAudio() { 
    missil.missilAudio.volume = 0;
    missil.explosionAudio.volume = 0;
    themeSong.pause();
    // missil.missilAudio.pause(); 
} 
function Transform(options = {
    position:[0,0],
    angle:0
}){
    options = options||{}
    options.position = options.position||[0,0];
    options.angle = options.angle||0;
    this.position = {x:options.position[0], y:options.position[1]};
    this.angle = options.angle;
    this.Compare = function(transform01){
        return (this.position.x == transform01.position.x)&&(this.position.y == transform01.position.y)&&(this.angle == transform01.angle)
    }
    this.CopyValue = function(transform01){
        this.position.x = transform01.position.x;
        this.position.y = transform01.position.y;
        this.angle = transform01.angle;
    }
}

class Controller{
    constructor() {
        this.time0 = Date.now();
        this.time1 = Date.now();
        this.deltaTime = (this.time1 - this.time0)/1000;
        this.objectsArray;   
    }
    
    // update(){
    //     this.time0 = this.time1;
    //     this.time1 = Date.now();
    //     this.deltaTime = this.time1 - this.time0;
    // }
    updateScene(){
        var n;
        // console.log("Flag01 Controller-UpdateScene");
        // console.log("Flag01-01 Controller-UpdateScene");  
        this.time0 = this.time1;
        this.time1 = Date.now();
        this.deltaTime = (this.time1 - this.time0)/1000;
        // console.log(aviao)
        //passa por todos os objetos
        // console.log(this.objectsArray);
        n = this.objectsArray.length;
        for (let index = 0; index < n; index++) {
            this.objectsArray[index].update();
        }
        //verifica colisões
        var num = n - 1;
        for (let i = 0; i < num; i++) {
            
            for (let j = i+1; j < n; j++) {
                this.objectsArray[i].collision(this.objectsArray[j])
                
            }
            if(this.objectsArray[i].toBeDestroyed){
                this.objectsArray[i].destroyItself();
                n--;
                num--;
                i--;
            }
        }
        if(num>0&&this.objectsArray[num].toBeDestroyed){
            this.objectsArray[num].destroyItself();
            n--;
            num--;
        }
        // contexto.clearRect( 0,0 , canvas.width, canvas.height);
        for (let index = 0; index < n; index++) {
            this.objectsArray[index].eraseDraw();
        }
        for (let index = 0; index < n; index++) {
            this.objectsArray[index].Draw();
        }
        // console.log("Flag02 Controller-UpdateScene");
    }
    printa(){
        console.log(this.objectsArray);
    }
}

var controller = new Controller();

class ObjetoImagem{
    constructor(options = {position:POSICAO, angle:ANGULO, imgLink:IMGLINK,
         fractionWidthCollision:WIDTH_FRACTION_AVIAO,fractionHeightCollision:HEIGHT_FRACTION_AVIAO}) {
        options = options||{};
        options.position = options.position||POSICAO;
        options.angle = options.angle||ANGULO;
        options.imgLink = options.imgLink||IMGLINK;
        options.imgLink = options.imgLink||IMGLINK;
        options.fractionHeightCollision = options.fractionHeightCollision||HEIGHT_FRACTION_AVIAO;
        options.fractionWidthCollision = options.fractionWidthCollision||WIDTH_FRACTION_AVIAO;
        this.transform = new Transform({position:options.position, angle:options.angle});
        this.transformZero = new Transform({position:options.position, angle:options.angle});
        this.sin = Math.sin(this.transform.angle*DEG2RAD);
        this.cos = Math.cos(this.transform.angle*DEG2RAD);
        this.sinZero = Math.sin(this.transformZero.angle*DEG2RAD);
        this.cosZero = Math.cos(this.transformZero.angle*DEG2RAD);
        this.img = new Image()
        this.onload = this.Draw;
        this.img.src = options.imgLink;
        this.imgZero = this.img;
        this.toBeDestroyed = false;
        this.fractionWidthCollision=options.fractionWidthCollision;
        this.fractionHeightCollision=options.fractionHeightCollision;
        
        console.log("this.colliderWidthHalf = ",this.colliderWidthHalf, " this.colliderHeightHalf = ", this.colliderHeightHalf);
    }
    eraseDraw(){
        //limpa parte do canvas do frame antigo
        contexto.save();
        
        contexto.rotate(this.transformZero.angle*DEG2RAD);
        contexto.clearRect( this.transformZero.position.x*this.cosZero + this.transformZero.position.y*this.sinZero - this.imgZero.naturalWidth/2-100,
            this.transformZero.position.y*this.cosZero - this.transformZero.position.x*this.sinZero - this.imgZero.naturalHeight/2-100,
            this.imgZero.naturalWidth+200, this.imgZero.naturalHeight+200);
        contexto.restore();
    }
    Draw(){
        // this.eraseDraw();
        //desenha imagem no canvas
        contexto.save();
        contexto.rotate(this.transform.angle*DEG2RAD);
        contexto.drawImage(this.img, this.transform.position.x*this.cos + this.transform.position.y*this.sin - this.img.naturalWidth/2,
            this.transform.position.y*this.cos - this.transform.position.x*this.sin - this.img.naturalHeight/2);
        contexto.restore();
        this.transformZero.CopyValue(this.transform);
        this.imgZero = this.img;
        this.sinZero = this.sin;
        this.cosZero = this.cos;
    }
    collision(objeto){
        return;
    }
    update(){
        return;
    }
    destroyItself(){
        if(this.toBeDestroyed){
            //apaga o desenho
            this.eraseDraw();
            controller.objectsArray.splice(controller.objectsArray.indexOf(this),1);
        }
    }
}

class AviaoObjeto extends ObjetoImagem{
    constructor(options = {position:POSICAO, angle:ANGULO, imgLink:AVIAOIMGLINK
        ,fractionWidthCollision:WIDTH_FRACTION_AVIAO,fractionHeightCollision:HEIGHT_FRACTION_AVIAO}) {
        options = options||{};
        options.imgLink = options.imgLink||AVIAOIMGLINK;
        options.fractionWidthCollision = options.fractionWidthCollision||WIDTH_FRACTION_AVIAO;
        options.fractionHeightCollision = options.fractionHeightCollision||HEIGHT_FRACTION_AVIAO;
        super(options);
        this.estado = MOVING_AVIAO;
        
    }
    update(){
        
        if(this.estado == MOVING_AVIAO){
            //Segue acompanha mouse
            this.transform.position.x = mousePos.x;
            this.transform.position.y = mousePos.y;
            //console.log("FlAG AviaoObjeto.transform = ", this.transform);
        }
    }
    collision(objeto){
        if(objeto instanceof MissilObjeto){
            objeto.collision(this);
        }
    }
}

class MissilObjeto extends ObjetoImagem{
    constructor(alvo, options = {velocity:VELOCITY_MISSIL,position:POSICAO, angle:ANGULO, imgLink:MISSILIMGLINK
        ,fractionWidthCollision:WIDTH_FRACTION_MISSILE,fractionHeightCollision:HEIGHT_FRACTION_MISSILE}) {
        options = options||{};
        options.imgLink = options.imgLink||MISSILIMGLINK;
        options.velocity = options.velocity||VELOCITY_MISSIL;
        options.fractionWidthCollision = options.fractionWidthCollision||WIDTH_FRACTION_MISSILE;
        options.fractionHeightCollision = options.fractionHeightCollision||HEIGHT_FRACTION_MISSILE;
        super(options);
        this.alvo = alvo;
        this.estado = IDLE_MISSIL;
        // this.estado = EXPLODING_MISSIL;
        this.velocity = options.velocity;
        this.missilAudio = new Audio(AUDIO_LINK_MISSIL);
        this.explosionAudio = new Audio(AUDIO_LINK_EXPLOSION);

        //prepara animação
        this.explosionAnimationFrames = [];
        this.framesDelayed = 0;
        this.frameAnimation = 0;
        for (let index = 0; index < 7; index++) {
            this.explosionAnimationFrames.push(new Image());
            this.explosionAnimationFrames[index].src = EXPLOSION_NAME_MISSIL + index.toString() + EXPLOSION_TYPE_MISSIL;
            
        }
        this.missilAudio.addEventListener('ended', function() {
            this.currentTime = 0;
            this.play();
        }, false);
        // this.missilAudio.play();
        console.log("FlAG MissilObjeto.transform = ", this.transform);
        this.explosionAudio.volume = VOLUME_EXPLOSION;

        this.missilAudio.volume = VOLUME_MISSIL;
    }
    collision(objeto){
        if(objeto instanceof AviaoObjeto && this.estado == FOLLOW_MISSIL){
            //tamanho do rect colisor
            var colliderWidthHalf = this.fractionWidthCollision*this.img.naturalWidth/2;
            var colliderHeightHalf = this.fractionHeightCollision*this.img.naturalHeight/2;


            var otherColliderWidthHalf = objeto.fractionWidthCollision*objeto.img.naturalWidth/2;
            var otherColliderHeightHalf = objeto.fractionHeightCollision*objeto.img.naturalHeight/2;

            //vamos calcular o angulo relativo ao objeto
            var angulo = this.transform.angle - objeto.transform.angle;
            var sin = Math.sin(angulo*DEG2RAD);
            var cos = Math.cos(angulo*DEG2RAD);
            // var objetoVertices = [];//vertices do objeto
            var vertices = [];
            for (let i = 0; i < 4; i++) {
                // objetoVertices.push({x:
                //     objeto.transform.position.x - (1 - 2*(i&1))*otherColliderWidthHalf,
                //         y:objeto.transform.position.y - (1 - (i&2))*otherColliderHeightHalf
                //     }
                // );
                vertices.push({x:
                    this.transform.position.x - (1 - 2*(i&1))*colliderWidthHalf*cos + (1 - (i&2))*colliderHeightHalf*sin,
                        y:this.transform.position.y - (1 - (i&2))*colliderHeightHalf*cos - (1 - 2*(i&1))*colliderWidthHalf*sin
                    }
                );
                
            }
            var dx;
            var dy;
            for (let i = 0; i < 4; i++) {
                dx = objeto.transform.position.x - vertices[i].x;
                dy = objeto.transform.position.y - vertices[i].y;
                if (dx < 0) {
                    dx *= -1;
                }
                if (dy < 0) {
                    dy *= -1;
                }
                if(dx < otherColliderWidthHalf&&dy < otherColliderHeightHalf){
                    objeto.toBeDestroyed = true;
                    this.estado = EXPLODING_MISSIL;
                    this.missilAudio.pause();

                    
                    this.explosionAudio.play();
                    return;
                }
                
            }

        }
    }
    update(){
        if(this.estado == FOLLOW_MISSIL){

            //Move no intervalo de tempo pequeno(Frame) como se o angulo fosse constante
            // console.log("FlAG MissilObjeto.transform = ", this.transform);
            this.transform.position.x += this.velocity*this.cos*controller.deltaTime;
            this.transform.position.y += this.velocity*this.sin*controller.deltaTime;
            // this.transform.position.x += this.velocity*this.cos*controller.deltaTime;
            // this.transform.position.y += this.velocity*this.sin*controller.deltaTime;
            // console.log("FlAG MissilObjeto.transform = ", this.transform);

        }else if(this.estado == EXPLODING_MISSIL){
            if(this.frameAnimation < this.explosionAnimationFrames.length){
                if(this.framesDelayed == 0){
                    if(this.frameAnimation == 0){
                        this.transform.position.x += this.img.naturalWidth*this.cos/2;
                        this.transform.position.y += this.img.naturalHeight*this.sin/2;
                    }
                    this.framesDelayed++;
                    this.img = this.explosionAnimationFrames[this.frameAnimation];
                    
                }
                else if(this.framesDelayed < FRAME_EXPLOSION_DELAY){
                    this.framesDelayed++;
                }else{
                    this.framesDelayed = 0;
                    this.frameAnimation++;
                }
            }else{
                this.toBeDestroyed = true;
            }
        }
        if(this.estado != EXPLODING_MISSIL){

            //Move Angulo
            var dx = this.alvo.transform.position.x - this.transform.position.x;
            var dy = this.alvo.transform.position.y - this.transform.position.y;
            var newAngle = (dx!=0)?Math.atan(dy/dx)/DEG2RAD:(
                (dy>0)?90:(
                    (dy<0)?-90:0
                )
            );
            if(dx < 0){
                newAngle -= 180;
            }
            this.transform.angle = newAngle;
            // console.log("FlAG MissilObjeto newAngle = ", newAngle);
            this.sin = Math.sin(newAngle*DEG2RAD);
            this.cos = Math.cos(newAngle*DEG2RAD);
        }
    }
}
var pageXOffsetResize;
var pageYOffsetResize;
window.addEventListener('resize', resizeCanvas, false);
function resizeCanvas() {
    console.log(rect);
    // canvas.width = window.innerWidth - rect.left;
    // canvas.height = window.innerHeight - rect.top; 
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight; 
    rect = canvas.getBoundingClientRect();
    pageXOffsetResize = window.pageXOffset;
    pageYOffsetResize = window.pageYOffset;
    console.log(canvas);
    console.log(rect);
    console.log(window);
}
function main(){

    console.log("Flag01 MAIN");
    canvas = document.getElementById("canvas");
    contexto = canvas.getContext('2d');
    resizeCanvas();
    console.log("Flag04 MAIN");
    console.log(window);
    canvas.addEventListener("mousemove",function(evt){
        // console.log("Flag04-01 MAIN-mousemove");
        mousePos.x = evt.clientX - rect.left - pageXOffsetResize + window.pageXOffset;
        mousePos.y = evt.clientY - rect.top - pageYOffsetResize + window.pageYOffset;
        // console.log("Flag04-02 MAIN-mousemove");
        // console.log("x = ",mousePos.x," y = ", mousePos.y);
    });
    canvas.addEventListener("click",function(evt){
        // console.log("Flag04-01 MAIN-mousemove");
        missil.estado = FOLLOW_MISSIL;
        missil.missilAudio.play();
        // console.log("Flag04-02 MAIN-mousemove");
        // console.log("x = ",mousePos.x," y = ", mousePos.y);
    });
    console.log("Flag05 MAIN");

    //musica tema
    themeSong = document.getElementById(THEME_SONG_ID);
    themeSong.volume = THEME_SONG_VOLUME;
    themeSong.addEventListener('ended', function() {
        this.currentTime = 0;
        this.play();
    }, false);
    
    console.log("Flag07 MAIN");

    //aviao
    aviao = new AviaoObjeto({
        position:[3*canvas.width/4,canvas.height/2]
    });
    // missil.transform.position.x = 3*canvas.width/4;
    // missil.transform.position.y = canvas.height/2;
    controller.objectsArray = [aviao];
    console.log(controller.objectsArray);
    console.log("Flag08 MAIN");

    //missil
    missil = new MissilObjeto(aviao,{
        position:[canvas.width/4,3*canvas.height/4],
        angle:-90
    });
    controller.objectsArray.push(missil);
    console.log(controller.objectsArray);
    console.log("Flag09 MAIN");

    
    // console.log("Missile on load")
    //Audio
    // missilAudio = document.getElementById("myMissile"); 
    
    //Controla loop
    setInterval(function(){controller.updateScene()}, 30);
    // controller.printa();
    console.log("Flag10 MAIN");
}
window.addEventListener('DOMContentLoaded', main);
window.addEventListener('mousedown',firstInterection);
function firstInterection(){
    themeSong.play();
    window.removeEventListener('mousedown',firstInterection);
}
// window.onload = main