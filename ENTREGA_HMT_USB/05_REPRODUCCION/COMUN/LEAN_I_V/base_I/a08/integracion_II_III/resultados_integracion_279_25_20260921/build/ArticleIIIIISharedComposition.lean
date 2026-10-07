import ArticleIIFromSharedBase
import ArticleIIIFromSharedBase

/-! The two article continuations use identical selected objects, not two
independently chosen angular or constitutive inputs. -/
noncomputable section
namespace HMT.Shared.ArticleIIIII

theorem same_angular_chamber :
    HMT.II.FromSharedBase.angles = HMT.Shared.ArticleIII.angles := rfl

theorem same_oriented_channels :
    HMT.II.FromSharedBase.channels = HMT.Shared.ArticleIII.channels := rfl

theorem same_barbero_functional :
    HMT.II.FromSharedBase.barberoValue = HMT.Shared.ArticleIII.gamma := rfl

theorem barbero_recovered_from_shared_vacuum :
    HMT.II.FromSharedBase.barberoValue =
      HMT.OrientedReturn.speedImpedanceFunctional
        HMT.Shared.ArticleIII.impedance HMT.Shared.ArticleIII.speed
        (HMT.OrientedReturn.vacuum_minus_reading_mem HMT.Shared.ArticleIII.channels)
        (HMT.OrientedReturn.vacuum_plus_reading_mem HMT.Shared.ArticleIII.channels) :=
  HMT.Shared.ArticleIII.gamma_from_constitutive_readings

end HMT.Shared.ArticleIIIII
end

#print axioms HMT.Shared.ArticleIIIII.same_angular_chamber
#print axioms HMT.Shared.ArticleIIIII.same_oriented_channels
#print axioms HMT.Shared.ArticleIIIII.same_barbero_functional
#print axioms HMT.Shared.ArticleIIIII.barbero_recovered_from_shared_vacuum
