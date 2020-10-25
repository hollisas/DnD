on('ready',()=>{

    const HandoutName = 'Char Stat Dump';
    const WriteAttrs = {
        hp: {
            curr_hp: 'current',
            max_hp: 'max'
        },
        ac: {
            ac: 'current'
        },
        initiative: {
            initiative: 'current'
        },
        level: {
            level: 'current'
        }
    };

    let OBSData = {};

    const assureCharacter = (key) => (OBSData[key]=OBSData[key]||{});
    const assureHandout = () => {
        return findObjs({
            type: 'handout',
            archived: false,
            name: HandoutName
        })[0] || createObj('handout',{
            name: HandoutName
        });
    };

    let OBSHandout = assureHandout();


    const isPlayerCharacter = (character) => {
        if(character){
            let players = character.get('controlledby').split(/,/).filter(s=>s.length);
            return  players.includes('all') || (players.filter((p)=>!playerIsGM(p)).length>0);
        }
        return false;
    };

    const isPlayerToken = (token) => {
        let players = token.get('controlledby')
            .split(/,/)
            .filter(s=>s.length);

        if( players.includes('all') || players.filter((p)=>!playerIsGM(p)).length ) {
           return true;
        } 

        if('' !== token.get('represents') ) {
            return isPlayerCharacter(getObj('character',token.get('represents')));
        }
        return false;
    };

    const writeOBSData = ()=>{
        if(OBSHandout){
            let j = JSON.stringify(OBSData);
            OBSHandout.set({
                notes: j,
                //gmnotes: j
            });
        }
    };

    const loadAttrDataFromAttr = (charKey, attr) => {
        let attrName=attr.get('name');
        Object.keys(WriteAttrs[attrName]).forEach(attrKey => {
            OBSData[charKey][attrKey]=attr.get(WriteAttrs[attrName][attrKey]);
        });
    };

    const loadAttrData = (charKey, charID, attrName) => {
        let attr = findObjs({
            type: 'attribute',
            name: attrName,
            characterid: charID
        })[0];
        if(attr){
            loadAttrDataFromAttr(charKey, attr);
        }
    };

    const loadCharacterData = (character) => {
        let key = character.get('name');
        assureCharacter(key);
        Object.keys(WriteAttrs).forEach(a=>loadAttrData(key,character.id,a));

    };

    const handleChangeAttribute = (obj,prev) => {
        if(WriteAttrs.hasOwnProperty(prev.name)){
            let c = getObj('character',prev._characterid);
            if(c && isPlayerCharacter(c)){
                let key = c.get('name');
                assureCharacter(key);
                loadAttrDataFromAttr(key,obj);

                writeOBSData();
            }
        }
    };

    const handleChangeCharacter = (obj,prev) => {
        if(isPlayerCharacter(obj)){
            // handle name change
            if(obj.get('name') != prev.name){
                OBSData[obj.get('name')]=OBSData[prev.name];
                delete OBSData[prev.name];

                writeOBSData();
            } else if( !OBSData.hasOwnProperty(obj.get('name'))){
                loadCharacterData(obj);
                writeOBSData();
            }
        } else {
            if(OBSData.hasOwnProperty(obj.get('name'))){
                delete OBSData[obj.get('name')];
                writeOBSData();
            }
        }
    };


    findObjs({
        type: 'character',
        archived: false
    }).filter(isPlayerCharacter)
    .forEach(loadCharacterData);

    writeOBSData();

    on('change:attribute',handleChangeAttribute);
    on('change:character',handleChangeCharacter);


});