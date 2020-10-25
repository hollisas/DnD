on('ready',()=>{
    
    const playerpages = Campaign().get('playerpageid');
    const page = getObj('page',playerpages);
    let nameOfMap = page.get('name');
    log(nameOfMap);
    
    const HandoutName = 'Map';
    const WriteAttrs = {
        name: {
            name: 'name'
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

    const writeOBSData = ()=>{
        if(OBSHandout){
            let j = JSON.stringify(nameOfMap);
            OBSHandout.set({
                notes: j,
                gmnotes: j
            });
        }
    };

    writeOBSData();

    on('change:campaign:playerpageid', function(){
        const playerpages = Campaign().get('playerpageid');
        const page = getObj('page',playerpages);
        let nameOfMap = page.get('name');
        log(nameOfMap);
        const HandoutName = 'Map';
        const WriteAttrs = {
            name: {
                name: 'name'
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

        const writeOBSData = ()=>{
            if(OBSHandout){
                let j = JSON.stringify(nameOfMap);
                OBSHandout.set({
                    notes: j,
                    gmnotes: j
                });
            }
        };
        writeOBSData();
    });
});