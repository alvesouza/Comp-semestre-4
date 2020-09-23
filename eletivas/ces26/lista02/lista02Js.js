// document.getElementById("demo").innerHTML = "<h1>Hello World!</h1>";
    // Pedro Alves de Souza Neto
    // Turma COMP21
const POSICAO = [0,0];
const ANGULO = 0;
const AVIAOIMGLINK = "aviao.png"; 
const IMGLINK = AVIAOIMGLINK;
const DEG2RAD = Math.PI/180;

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
const MISSILIMGLINK = "aviao.png";
const VELOCITY_MISSIL = 10;
var canvas;
var contexto;

var aviao;
var mousePos;
var rect;
function Transform(options = {
    position:[0,0],
    angle:0
}){
    options = options||{}
    options.position = options.position||[0,0];
    this.position = {x:options.position.x, y:options.position.y};
    this.angle = options.angle||0;
    this.Compare = function(transform01){
        return (this.position.x == transform01.position.x)&&(this.position.y == transform01.position.y)&&(this.angle == transform01.angle)
    }
    this.CopyValue = function(transform01){
        this.position.x = transform01.position.x;
        this.position.y = transform01.position.y;
        this.angle = transform01.angle;
    }
}

function Controller(){
    this.time0 = Date.now();
    this.time1 = Date.now();
    this.deltaTime = this.time1 - this.time0;
    this.objectsArray = [];
    this.update = function(){
        this.time0 = this.time1;
        this.time1 = Date.now();
        this.deltaTime = this.time1 - this.time0;
    }
    this.UpdateScene = function(){
        var n;
        for(;;){    
            this.update();

            //passa por todos os objetos
            n = this.objectsArray.length;
            for (let index = 0; index < n; index++) {
                this.objectsArray[index].update();
                if(this.objectsArray[index].toBeDestroyed){
                    this.objectsArray[index].destroyItself();
                    n--;
                    index--;
                }
            }
        }
    }
}

class Classe{
    constructor(i) {
        this.x = i;
        this.dobro = this.Dobro;
    }
    Dobro(){
        return this.x*2;
    }
}

class Classe01 extends Classe{
    constructor(i) {
        super(i);
        this.dobro = this.Dobro;
    }
    Dobro(){
        return super.Dobro()*3;
    }
}
var classe = new Classe01(2);
console.log(classe.dobro());
var controller = new Controller();
var tranform = new Transform({position:[1,2],angle:30})
var tranform1 = new Transform({position:[1,1],angle:30})
console.log(tranform)
console.log(tranform1)
console.log(tranform1.Compare(tranform))

class ObjetoImagem{
    constructor(options = {position:POSICAO, angle:ANGULO, imgLink:IMGLINK}) {
        options = options||{};
        options.position = options.position||POSICAO;
        options.angle = options.angle||ANGULO;
        options.imgLink = options.imgLink||IMGLINK;
        this.transform = new Transform({position:options.position, angle:options.angle});
        this.transformZero = new Transform({position:options.position, angle:options.angle});
        this.sin = Math.sin(this.transform.angle*Math.PI/180);
        this.cos = Math.cos(this.transform.angle*Math.PI/180);
        this.sinZero = Math.sin(this.transformZero.angle*DEG2RAD);
        this.cosZero = Math.cos(this.transformZero.angle*DEG2RAD);
        this.img = new Image()
        this.onload = this.Draw;
        this.img.src = options.imgLink;
        this.toBeDestroyed = false;
    }
    eraseDraw(){
        //limpa parte do canvas do frame antigo
        contexto.save();
        
        contexto.rotate(this.transformZero.angle*DEG2RAD);
        contexto.clearRect( this.transformZero.position.x*this.cosZero + this.transformZero.position.y*this.sinZero - this.img.naturalWidth/2,
            this.transformZero.position.y*this.cosZero - this.transformZero.position.x*this.sinZero - this.img.naturalHeight/2,
             this.img.naturalWidth, this.img.naturalHeight);
        contexto.restore();
    }
    Draw(){
        this.eraseDraw();

        //desenha imagem no canvas
        contexto.save();
        contexto.rotate(this.transform.angle*DEG2RAD);
        contexto.drawImage(aviao, this.transform.position.x*this.cos + this.transform.position.y*this.sin - this.img.naturalWidth/2,
            this.transform.position.y*this.cos - this.transform.position.x*this.sin - this.img.naturalHeight/2);
        contexto.restore();
        this.transformZero.CopyValue(this.transform);
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
    constructor(options = {position:POSICAO, angle:ANGULO, imgLink:AVIAOIMGLINK}) {
        options = options||{};
        options.imgLink = options.imgLink||AVIAOIMGLINK;
        super(options);
        this.estado = MOVING_AVIAO;
    }
    update(){
        
        if(this.estado == MOVING_AVIAO){
            //Segue acompanha mouse
            this.transform.x = 0;
            this.transform.y = 0;
        }
    }
}

class MissilObjeto extends ObjetoImagem{
    constructor(alvo, options = {velocity:VELOCITY_MISSIL,position:POSICAO, angle:ANGULO, imgLink:MISSILIMGLINK}) {
        options = options||{};
        options.imgLink = options.imgLink||MISSILIMGLINK;
        options.velocity = options.velocity||VELOCITY_MISSIL;
        super(options);
        this.alvo = alvo;
        this.estado = IDLE_MISSIL;
    }
    update(){
        if(this.estado == FOLLOW_MISSIL){

            //Move no intervalo de tempo pequeno(Frame) como se o angulo fosse constante
            this.transform.position.x += this.velocity*this.cos*controller.deltaTime;
            this.transform.position.y += this.velocity*this.sin*controller.deltaTime;

            //Move Angulo
            var dx = this.alvo.transform.x - this.transform.x;
            var dy = this.alvo.transform.y - this.transform.y;
            var newAngle = (dx!=0)?Math.atan(dy/dx)/DEG2RAD:(
                (dy>0)?90:(
                    (dy<0)?-90:0
                )
            );
            if(dx < 0){
                newAngle -= 180;
            }
            this.transform.angle = newAngle;

        }
    }
}

function main(){
    canvas = document.getElementById("canvas");
    contexto = canvas.getContext('2d');
    rect = canvas.getBoundingClientRect();
    canvas.addEventListener("mousemove",function(evt){
        mousePos = {x:evt.clientX - rect.left, y:evt.clientY - rect.top};
        // console.log("x = ",mousePos.x," y = ", mousePos.y);
    });
    aviao = new AviaoObjeto();
    missil = new MissilObjeto(aviao);
    controller.objectsArray.push(aviao);
    controller.objectsArray.push(missil);

    controller.UpdateScene();
}
window.onload = main

function caiTexto(objeto, option = {intervalo:5, posFinalRelativa:110}) {
    var option = option||{};
    option.intervalo = option.intervalo||5;
    posFinalRelativa = option.posFinalRelativa||110;
    // console.log("Flag01");
    var posInicial = objeto.getBoundingClientRect().y;
    // console.log("Flag02 posInicial = " + posInicial);
    var aux = window.innerHeight;
    var pos= 100*posInicial/aux;
    posInicial = pos;
    var velocidade = (posFinalRelativa - pos)/(option.intervalo*1000);
    var time01 = Date.now();
    var time02;
    var dt;
    var id = setInterval(function() {
        time02 = Date.now();
        dt = time02 - time01;
        // console.log("Flag07 dt = " + dt);
        if (pos >= posFinalRelativa) {
            objeto.style.top = posInicial + "%"; 
            clearInterval(id);
        }  else {
            pos=pos+velocidade*dt; 
            // console.log("Flag09 objeto.style.top = " + objeto.style.top);
            objeto.style.top = pos + "%"; 
        }
        time01 = time02;
    }, 5);
    
}