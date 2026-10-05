"""Original synthetic, anonymous fixtures. No vendor examples or measurement catalog."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'fixtures'; F.mkdir(exist_ok=True)
T='''<?xml version="1.0" encoding="UTF-8"?>
<smis>
  <version>0.3.4</version>
  <read-only>false</read-only>
  <notes/>
  <unit>cm</unit>
  <pm_system>998</pm_system>
  <personal>
    <family-name/>
    <given-name/>
    <birth-date>1800-01-01</birth-date>
    <gender>unknown</gender>
    <email/>
  </personal>
  <body-measurements>
    <m name="@girth" value="80" full_name="Synthetic girth" description="Original test dimension"/>
    <m name="@length" value="50" full_name="Synthetic length" description="Original test dimension"/>
    <m name="@ease" value="2" full_name="Fixed allowance" description="Keep this numeric constant"/>
    <m name="@quarter" value="@girth/4+@ease" full_name="Derived width" description="Protected formula"/>
    <m name="@halfLength" value="@length/2" full_name="Derived height" description="Protected formula"/>
  </body-measurements>
</smis>
'''
(F/'anonymous.smis').write_text(T)
(F/'rows.csv').write_text('row_id,unit,girth,length\nA,cm,80,50\nB,mm,900,600\nC,inch,40,24\n')
# A four-point rectangular native pattern authored specifically for this gate.
(F/'rectangle.sm2d').write_text('''<?xml version="1.0" encoding="UTF-8"?>
<pattern>
  <version>0.7.5</version>
  <unit>cm</unit>
  <description>Original synthetic formula consumer. No garment or fit claim.</description>
  <notes/>
  <measurements>anonymous.smis</measurements>
  <variables/>
  <draftBlock name="Synthetic rectangle">
    <calculation>
      <point id="1" type="single" name="A" x="0" y="0" mx="0" my="0"/>
      <point id="2" type="endLine" name="B" basePoint="1" angle="0" length="@quarter" lineColor="black" lineType="solidLine" mx="0" my="0"/>
      <point id="3" type="endLine" name="C" basePoint="2" angle="270" length="@halfLength" lineColor="black" lineType="solidLine" mx="0" my="0"/>
      <point id="4" type="endLine" name="D" basePoint="1" angle="270" length="@halfLength" lineColor="black" lineType="solidLine" mx="0" my="0"/>
    </calculation>
    <modeling>
      <point id="5" idObject="1" type="modeling" inUse="true" mx="0" my="0"/>
      <point id="6" idObject="2" type="modeling" inUse="true" mx="0" my="0"/>
      <point id="7" idObject="3" type="modeling" inUse="true" mx="0" my="0"/>
      <point id="8" idObject="4" type="modeling" inUse="true" mx="0" my="0"/>
    </modeling>
    <pieces>
      <piece id="9" name="Formula rectangle" version="2" closed="1" mx="0" my="0" seamAllowance="false" width="0" inLayout="true">
        <data visible="false"/>
        <patternInfo visible="false"/>
        <grainline visible="false"/>
        <nodes>
          <node idObject="5" type="NodePoint"/>
          <node idObject="6" type="NodePoint"/>
          <node idObject="7" type="NodePoint"/>
          <node idObject="8" type="NodePoint"/>
        </nodes>
      </piece>
    </pieces>
  </draftBlock>
</pattern>
''')
